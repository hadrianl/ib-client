<template>
    <v-form v-model="valid">
        <v-list dense>
            <v-list-group :value="false">
                <template v-slot:activator>
                    <v-list-item-content>
                        <v-list-item-title>参考成本</v-list-item-title>
                    </v-list-item-content>
                </template>
                <v-list-item-group v-model="cost">
                    <v-list-item :value="openCost">
                        参考开仓成本：{{ openCost[1] }}@{{ parseInt(openCost[1]!=0?openCost[0]/openCost[1]:openCost[0]) }}
                    </v-list-item>
                    <v-list-item :value="sessionCost">
                        参考会话成本：{{ sessionCost[1] }}@{{ parseInt(sessionCost[1]!=0?sessionCost[0]/sessionCost[1]:sessionCost[0]) }}
                    </v-list-item>
                    <v-list-item :value="totalCost">
                        参考总成本  ：{{ totalCost[1] }}@{{ parseInt(totalCost[1]!=0?totalCost[0]/totalCost[1]:totalCost[0]) }}
                    </v-list-item>
                </v-list-item-group>    
            </v-list-group> 
        </v-list>
        <v-list dense>                
            <v-list-item>
                <v-text-field 
                v-model="costOffset" 
                label="costOffset" 
                type="number"
                :rules="offsetRules"
                outlined 
                dense></v-text-field>
            </v-list-item>  
            <v-list-item>
                <v-text-field v-model="trailStopPrice" label="trailStopPrice" type="number" :rules="priceRules" outlined dense></v-text-field>
                <v-text-field 
                v-model="volume"
                prepend-icon="mdi-location-enter"
                label="volume" 
                type="number"
                :rules="priceRules"
                outlined
                dense>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-text-field v-model="trailAmount" label="trailAmount" type="number" :rules="priceRules" outlined dense>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-up-circle':'mdi-arrow-down-circle':''}}</v-icon>
                    </template>
                </v-text-field>
                <v-text-field 
                v-model="lmtPriceOffset" 
                label="lmtPriceOffset" 
                type="number"
                :rules="offsetRules"
                outlined
                dense>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-up-circle':'mdi-arrow-down-circle':''}}</v-icon>
                    </template>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-text-field v-model="orderRef" label="orderRef" placeholder="Order Ref" clearable dense></v-text-field>
            </v-list-item>
            <v-list-item>
                <v-btn-toggle
                v-model="action" 
                rounded 
                dense
                class="mx-auto pm-auto">
                    <v-btn value="BUY" color="red">BUY</v-btn>
                    <v-btn value="SELL" color="green">SELL</v-btn>
                </v-btn-toggle>
            </v-list-item>
            <v-list-item>
                <v-row justify="space-around">
                    <v-col cols="8">
                        <v-btn 
                        block
                        @click="insertOrder()" 
                        :color="action?action=='BUY'?'red':'green':''"
                        :disabled="!action"
                        >{{action?action:"NotSet"}}</v-btn>
                    </v-col>
                    <v-col cols="4">
                        <v-btn 
                        block
                        @click="reset()" >RESET</v-btn>
                    </v-col>  
                </v-row>
            </v-list-item>
        </v-list>
    </v-form>


</template>
<script>
import {Order} from '../../plugins/datastructure.js'
// import ContractItem from '../ContractItem.vue'
// import ContractItemVue from '../ContractItem.vue'
// const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    components:{
        // ContractItem
    },
    data() {
			return {
                action: undefined,
				volume: "1",
                priceTick: 1,
                costOffset: "60",
                cost: null,
                trailStopPrice: "0",
                trailAmount: "0",
                lmtPriceOffset: "0",
                orderRef: "",
                priceRules: [
                    v => v > 0,
                ],
                offsetRules: [
                ],
                valid: false,
			};
        },
    mounted() {
        this.$bus.$on('attachPrice', this.setOrderBaseOnAttachPrice)
    },
    watch: {
        cost(val) {
            if (val) {
                this.setOrderBaseOnCost(val)
            }
        },
        costOffset() {
            if (this.cost) {
                this.setOrderBaseOnCost(this.cost)
            }
        }
    },
    computed: {
        contract() {
            return this.$store.state.currentContract
        },
        openCost() {
            return this.$store.getters.currentOpenCost
        },
        sessionCost() {
            return this.$store.getters.currentSessionCost
        },
        totalCost() {
            return this.$store.getters.currentTotalCost
        },
    },
    beforeDestroy() {
        this.$bus.$off('attachPrice', this.setOrderBaseOnAttachPrice)
	},
    methods: {
        insertOrder() {
            // const contract = this.$refs.contract.currentContract
            const contract = this.contract
            if (contract == null) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择合约",
                    timeout: 2000
                })
                return
            }

            if (!this.action) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择方向",
                    timeout: 2000
                })
                return

            }

            var order = new Order()
            order.outsideRth = true
            order.orderType = 'TRAIL LIMIT'
            // order.tif = 'GTC'
            order.trailStopPrice = parseInt(this.trailStopPrice)
            order.lmtPriceOffset = parseInt(this.lmtPriceOffset)
            order.auxPrice = parseInt(this.trailAmount)
            order.action = this.action
            order.totalQuantity = parseInt(this.volume)
            order.triggerMethod = 4
            order.orderRef = this.orderRef
            console.log({'action': 'place_order', 'contract': contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': contract, 'order': order})


        },
        setOrderBaseOnCost(cost){
            console.log(cost)
            if(!cost[1]){
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Set Order Ref failed!',
                    content: "无法参考0持仓设置止损单",
                    timeout: 4000
                })
                this.cost = null
                return
            }

            this.volume = Math.abs(cost[1])
            const avgCost = parseInt(cost[0]/cost[1])
            const costOffset = parseInt(this.costOffset)
            this.trailStopPrice = cost[1]>0? avgCost - costOffset:avgCost + costOffset
            this.trailAmount = this.costOffset
            this.action = cost[1]>0?"SELL":"BUY"
            this.orderRef = `trailsl-${this.volume}@${avgCost}`
        },
        setOrderBaseOnAttachPrice(price) {
            if (!this.action) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择方向",
                    timeout: 2000
                })
                return
            }

            const costOffset = parseInt(this.costOffset)
            this.trailStopPrice = this.action == 'BUY'? price + costOffset: price - costOffset
            this.trailAmount = costOffset
            this.orderRef = `trailsl-${this.volume}@${price}`
        },
        reset() {
            this.volume = "1"
            this.trailStopPrice = "0"
            this.lmtPriceOffset = "0"
            this.trailAmount = "0"
            this.action = undefined
            this.costOffset = "60"
        },
		}
}
</script>