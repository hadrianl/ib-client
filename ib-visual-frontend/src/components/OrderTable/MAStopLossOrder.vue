<template>
    <Form :label-width="60" label-position="left">
        <ContractItem ref="contract" :contractsList=contractsList />
        <FormItem label="Size">
            <InputNumber v-model="volume" :min="1" style="width: auto"></InputNumber>
        </FormItem>
        <FormItem label="Trigger" inline>
            <Input v-model="trigger" placeholder="触发类型..." />
            <Icon v-if="action == 'BUY'" type="ios-arrow-round-up" color="red" />
            <Icon v-else-if="action == 'SELL'" type="ios-arrow-round-down" color="green" />
            <Icon v-else type="ios-help" />
            <InputNumber v-model="offset" :max="maxOffset" :min="minOffset" :step="priceTick" ></InputNumber>
        </FormItem>
        <FormItem label="Action">
            <RadioGroup v-model="action" type="button" >
                <Radio label="BUY" style="color:red"></Radio>
                <Radio label="SELL" style="color:green"></Radio>
            </RadioGroup>
        </FormItem>
        <FormItem>
            <Button @click="insertOrder()" size="large" style="background:blue">{{action?action:"Not Set"}}</Button>
            <Button @click="reset()" style="margin-left: 8px" size="large">RESET</Button>
        </FormItem>
	</Form>
</template>
<script>
import {Order} from '../../plugins/datastructure.js'
import ContractItem from '../ContractItem.vue'


export default {
    components:{
        ContractItem
    },
    data() {
			return {
                split: 0.3,
                action: "",
				volume: 1,
                priceTick: 1,
                trigger: '',
                offset: 0,
                maxOffset: 200,
                minOffset: 0,
			};
        },
    props:{
        contractsList: Array,
    },
    mounted() {

    },
    computed: {
        limitPrice: function() {
            switch (this.action) {
                    case "BUY":
                        return this.stopPrice + this.offset
                    case "SELL":
                        return this.stopPrice - this.offset
                    default:
                        return 0
                }
        }
    },
    methods: {
        insertOrder() {
            const contract = this.$refs.contract.currentContract
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

            const options = this.getTriggerOptions()

            if (!options) {
                this.$Notice.error({
                    title: 'order Failed!',
                    desc: '请填写正确触发类型',
                    duration: 5
                })
                return
            }

            
            var order = new Order()
            order.orderType = 'STP LMT'
            order.action = this.action
            order.totalQuantity = this.volume
            console.log({'action': 'place_dynamic_order', 'contract': contract, 'order': order, 'options': {}})
            this.$ibws.send({'action': 'place_dynamic_order', 'contract': contract, 'order': order, 'options': options})


        },
        reset() {
            this.$refs.contract.currentContract = null
            this.volume = 1
            this.stopPrice = 0
            this.offset = 0
            this.action = ""
        },
        getTriggerOptions() {
            const ma_trigger_patt = /^(ma)(\d+)$/i
            let trigger = this.trigger
            let ret = ma_trigger_patt.exec(trigger)
            let options = {}
            if (ret) {
                console.log(ret)
                const trigger_type = ret[1].toUpperCase()
                switch (trigger_type) {
                    case 'MA': {
                        let period = Number(ret[2])
                        if (0 < period <= 120) {
                            options['type'] = trigger_type
                            options['period'] = period
                            options['offset'] = this.offset
                        }
                        break
                    }
                }
            }
            return options
        }
		}
}
</script>