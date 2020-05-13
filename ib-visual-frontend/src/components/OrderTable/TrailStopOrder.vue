<template>
    <v-form v-model="valid">
        <v-list dense>                
            <v-list-item>
                <v-text-field 
                v-model.number="attachOffset" 
                label="attachOffset" 
                type="number"
                :rules="offsetRules"
                outlined 
                dense></v-text-field>
            </v-list-item>  
            <v-list-item>
                <v-text-field v-model.number="trailStopPrice" label="trailStopPrice" type="number" :rules="priceRules" outlined dense></v-text-field>
                <v-text-field 
                v-model.number="volume"
                prepend-icon="mdi-location-enter"
                label="volume" 
                type="number"
                :rules="priceRules"
                outlined
                dense>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-text-field v-model.number="trailAmount" label="trailAmount" type="number" :rules="priceRules" outlined dense>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-up-circle':'mdi-arrow-down-circle':''}}</v-icon>
                    </template>
                </v-text-field>
                <v-text-field 
                v-model.number="lmtPriceOffset" 
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
import {DEFAULT_CONFIG} from '../../plugins/utils.js'
export default {
    components:{
        // ContractItem
    },
    data() {
        return {
            action: undefined,
            volume: 1,
            attachPrice: 0,
            attachOffset: 60,
            cost: null,
            trailStopPrice: 0,
            trailAmount: 0,
            lmtPriceOffset: 0,
            orderRef: "",
            priceRules: [
                v => v > 0,
            ],
            offsetRules: [
            ],
            valid: false,
        }
    },
    mounted() {
        this.$bus.$on('attachPrice', this.setOrderBaseOnAttachPrice)
        this.$bus.$on('costReference', this.setOrderBaseOnCost)
        Object.assign(this.$data, DEFAULT_CONFIG['TrailStopOrder'])
    },
    watch: {
        attachOffset(nVal) {
            // console.log(nVal)
            // console.log(oVal)
            if (!(this.attachPrice&&nVal)) {
                return
            }
            switch(this.action) {
                case 'BUY':
                    this.trailStopPrice = this.attachPrice + nVal
                    this.trailAmount = this.attachOffset
                    break
                case 'SELL':
                    this.trailStopPrice = this.attachPrice - nVal
                    this.trailAmount = this.attachOffset
                    break
                default:
            }
        }
    },
    computed: {
        contract() {
            return this.$store.state.currentContract
        },
    },
    beforeDestroy() {
        this.$bus.$off('attachPrice', this.setOrderBaseOnAttachPrice)
        this.$bus.$off('costReference', this.setOrderBaseOnCost)
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
            order.tif = 'GTC'
            order.trailStopPrice = parseInt(this.trailStopPrice)
            order.lmtPriceOffset = parseInt(this.lmtPriceOffset)
            order.auxPrice = parseInt(this.trailAmount)
            order.action = this.action
            order.totalQuantity = parseInt(this.volume)
            order.triggerMethod = 4
            const ref = `trailsl-${order.totalQuantity}@^${order.trailStopPrice}->${order.auxPrice}[${order.lmtPriceOffset}]`
            order.orderRef = ref + '-' +this.orderRef
            this.orderRef = ''
            console.log({'action': 'place_order', 'contract': contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': contract, 'order': order})


        },
        setOrderBaseOnCost(cost){
            this.volume = Math.abs(cost[1])
            this.attachPrice = cost[0]/cost[1]
            const avgCost = this.attachPrice
            const attachOffset = this.attachOffset
            this.trailStopPrice = cost[1]>0? avgCost - attachOffset:avgCost + attachOffset
            this.trailAmount = attachOffset
            this.action = cost[1]>0?"SELL":"BUY"
            this.orderRef = `Cost<@${avgCost}>`
        },
        setOrderBaseOnAttachPrice(price) {
            if(!price) return
            if (!this.action) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择方向",
                    timeout: 2000
                })
                return
            }

            this.attachPrice = price
            const attachOffset = this.attachOffset
            this.trailStopPrice = this.action == 'BUY'? price + attachOffset: price - attachOffset
            this.trailAmount = attachOffset
            this.orderRef = `Cost<@${this.attachPrice}>`
        },
        reset() {
            this.volume = 1
            this.trailStopPrice = 0
            this.lmtPriceOffset = 0
            this.trailAmount = 0
            this.action = undefined
            this.attachPrice = 0
            this.attachOffset = 60
        },
		}
}
</script>