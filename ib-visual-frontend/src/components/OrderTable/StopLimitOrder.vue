<template>
    <v-form v-model="valid">
        <v-list dense>
            <v-list-item>
                <v-text-field 
                v-model.number="attachOffset" 
                label="attachOffset" 
                type="number"
                outlined 
                dense></v-text-field>
            </v-list-item>    
            <v-list-item>
                <v-text-field v-model.number="limitPrice" label="limitPrice" type="number" :rules="priceRules" disabled outlined dense></v-text-field>
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
                <v-text-field v-model.number="stopPrice" label="stopPrice" type="number" :rules="priceRules" outlined dense></v-text-field>
                <v-text-field 
                v-model.number="offset" 
                label="offset" 
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
                    <v-btn value="BUY" color="red">{{$t('button.buy')}}</v-btn>
                    <v-btn value="SELL" color="green">{{$t('button.sell')}}</v-btn>
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
                        >{{action?$t(`button.${action.toLowerCase()}`):$t('button.notSet')}}</v-btn>
                    </v-col>
                    <v-col cols="4">
                        <v-btn 
                        block
                        @click="reset()">{{$t('button.reset')}}</v-btn>
                    </v-col>  
                </v-row>
            </v-list-item>
        </v-list>
    </v-form>
</template>
<script>
import {Order} from '../../plugins/datastructure.js'
import axios from '../../plugins/axios.js'
export default {
    components:{
        // ContractItem
    },
    data() {
        return {
            action: undefined,
            volume: 1,
            stopPrice: 0,
            offset: 5,
            orderRef: "",
            attachOffset: 60,
            attachPrice: 0,
            priceRules: [
                v => v > 0,
            ],
            offsetRules: [
            ],
            valid: false,
        }
    },
    mounted() {
        // this.$bus.$on('attachPrice', this.setOrderBaseOnAttachPrice)
        // this.$bus.$on('costReference', this.setOrderBaseOnCost)
        axios.get('/config/default.json').then((response) => {Object.assign(this.$data, response.data['StopLimitOrder'])})
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
                    this.stopPrice = this.attachPrice + nVal
                    break
                case 'SELL':
                    this.stopPrice = this.attachPrice - nVal
                    break
                default:
            }
        }
    },
    computed: {
        limitPrice() {
            const sp = this.stopPrice
            const offset = this.offset
            switch (this.action) {
                    case "BUY":
                        return sp + offset
                    case "SELL":
                        return sp - offset
                    default:
                        return 0
                }
        },
        contract() {
            return this.$store.state.currentContract
        },
    },
    beforeDestroy() {
        // this.$bus.$off('attachPrice', this.setOrderBaseOnAttachPrice)
        // this.$bus.$off('costReference', this.setOrderBaseOnCost)
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

            if (!this.valid) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请正确填写下单参数",
                    timeout: 2000
                })
                return
            }

            var order = new Order()
            order.outsideRth = true
            order.orderType = 'STP LMT'
            order.tif = 'GTC'
            order.lmtPrice = parseInt(this.limitPrice)
            order.auxPrice = parseInt(this.stopPrice)
            order.action = this.action
            order.totalQuantity = parseInt(this.volume)
            const ref = `sl-${order.totalQuantity}@${order.auxPrice}->${order.lmtPrice}`
            order.orderRef = ref + '-' + this.orderRef
            console.log({'action': 'place_order', 'contract': contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': contract, 'order': order})


        },
        setOrderBaseOnCost(cost) {
            this.volume = Math.abs(cost[1])
            this.attachPrice = cost[0]/cost[1]
            const avgCost = this.attachPrice
            const attachOffset = this.attachOffset
            this.stopPrice = cost[1]>0? avgCost - attachOffset:avgCost + attachOffset
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
            this.stopPrice = this.action == 'BUY'? price + attachOffset: price - attachOffset
            this.orderRef = `Attach<@${this.attachPrice}>`

        },
        reset() {
            // this.$refs.contract.currentContract = null
            this.volume = 1
            this.stopPrice = 0
            this.offset = 5
            this.action = undefined
            this.attachPrice = 0
            this.attachOffset = 60
            axios.get('/config/default.json').then((response) => {Object.assign(this.$data, response.data['StopLimitOrder'])})
            // this.cost = null
        },
		}
}
</script>