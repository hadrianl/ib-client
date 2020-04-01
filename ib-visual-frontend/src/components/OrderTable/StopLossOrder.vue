<template>
    <Form :label-width="60" label-position="left">
        <!-- <ContractItem ref="contract" :contractsList="contractsList" /> -->
        <FormItem label="Size">
            <InputNumber v-model="volume" :min="1" style="width: auto"></InputNumber>
        </FormItem>
        <FormItem label="Price">
            <InputNumber v-model="limitPrice" disabled :max="maxPrice" :min="minPrice" :step="priceTick" style="width: auto"></InputNumber>
        </FormItem>
        <FormItem label="StopPrice" inline>
            <InputNumber v-model="stopPrice" :max="maxPrice" :min="minPrice" :step="priceTick"></InputNumber>
            <Icon v-if="action == 'BUY'" type="ios-arrow-round-up" color="red" />
            <Icon v-else-if="action == 'SELL'" type="ios-arrow-round-down" color="green" />
            <Icon v-else type="ios-help" />
            <InputNumber v-model="offset"   :max="200" :min="minPrice" :step="priceTick" ></InputNumber>
        </FormItem>
        <FormItem label="Action">
            <RadioGroup v-model="action" type="button" size="large">
                <Radio label="BUY" style="color:red"></Radio>
                <Radio label="SELL" style="color:green"></Radio>
            </RadioGroup>
        </FormItem>
        <FormItem>
            <Button @click="insertOrder()" size="large" :style="actionStyle">{{action?action:"NotSet"}}</Button>
            <Button @click="reset()" style="margin-left: 8px" size="large">RESET</Button>
        </FormItem>
	</Form>
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
                split: 0.3,
                selectedTab: 'accounts', // accounts positions orders trades
                action: "",
				volume: 1,
                priceTick: 1,
                stopPrice: 0,
                offset: 0,
				priceDecs: 0,
                maxPrice: Infinity,
                minPrice: 0,
			};
        },
    mounted() {

    },
    computed: {
        limitPrice() {
            switch (this.action) {
                    case "BUY":
                        return this.stopPrice + this.offset
                    case "SELL":
                        return this.stopPrice - this.offset
                    default:
                        return 0
                }
        },
        actionStyle() {
            switch (this.action) {
            case "BUY":
                return {
                    background: 'red'
                }
            case "SELL":
                return {
                    background: 'green'
                }
            default:
                return {
                    background: 'white'
                }
        }
        },
        contract() {
            return this.$store.state.currentContract
        }
    },
    methods: {
        insertOrder() {
            // const contract = this.$refs.contract.currentContract
            const contract = this.contract
            if (contract == null) {
                this.$Notice.error({
                    title: 'Order Failed!',
                    desc: "请先选择合约",
                    duration: 5
                })
                return
            }

            if (this.action == "") {
                this.$Notice.error({
                    title: 'Order Failed!',
                    desc: "请先选择方向",
                    duration: 5
                })
                return

            }

            var order = new Order()
            order.orderType = 'STP LMT'
            order.lmtPrice = this.limitPrice
            order.auxPrice = this.stopPrice
            order.action = this.action
            order.totalQuantity = this.volume
            console.log({'action': 'place_order', 'contract': contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': contract, 'order': order})


        },
        reset() {
            // this.$refs.contract.currentContract = null
            this.volume = 1
            this.stopPrice = 0
            this.offset = 0
            this.action = ""
        },
		}
}
</script>