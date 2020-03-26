<template>
    <Form :label-width="60" label-position="left">
        <FormItem label="Contract" inline>
            <AutoComplete clearable	
            icon="ios-search"
            v-model="condName" 
            :data="contractsList" 
            @on-search="querySearch" 
            @on-select="selectContract"
            @on-clear="clearContract"
            placeholder="请输入合约" >
            <Option v-for="(c, index) in contractsList" :value="c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4)" :key="index">
                <span>{{c.symbol}}{{c.lastTradeDateOrContractMonth.substr(2, 4)}} conId:{{c.conId}} </span>
            </Option>
            </AutoComplete>
        </FormItem>
        <Alert v-if="currentContract" type="success" show-icon>ConId：{{currentContract.conId}}</Alert>
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
import {Contract, Order} from '../../plugins/datastructure.js'
const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    data() {
			return {
                split: 0.3,
                condName: "",
                contractsList: [],
                selectedTab: 'accounts', // accounts positions orders trades
                action: "",
				volume: 1,
                priceTick: 1,
                stopPrice: 0,
                offset: 0,
				priceDecs: 0,
                maxPrice: Infinity,
                currentContract: null,
                minPrice: 0,
			};
        },
    mounted() {
        var _this = this
        this.$ibws.on('contract', function(c) {
            var flag = true
            _this.contractsList.forEach(element => {
                if (element.conId === c.conId){
                    flag = false
                }
            })
            if (flag){
                _this.contractsList.push(c)
            }
        })
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
			querySearch(queryString) {
                var ret = patt.exec(queryString)
                if (ret) {
                    let flag = true
                    this.contractsList.forEach(function(c){
                    if ((c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4)) === ret[0]){
                        flag = false
                    }
                    })

                    if (flag){
                        var c = new Contract()
                        c.secType = 'FUT'
                        c.symbol = ret[1].toUpperCase()
                        c.lastTradeDateOrContractMonth = '20' + ret[2]
                        this.$ibws.send({'action': 'get_contracts', 'data': c})
                    }
   
                }
            },
			selectContract(item) {
                var contract = null
                this.contractsList.forEach(function(c){
                    if ((c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4)) === item){
                        contract = c
                    }
                })
                this.currentContract = contract
            },
            clearContract() {
                this.currentContract = null
            },
			insertOrder() {
				if (this.currentContract == null) {
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

                var contract = this.currentContract
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
                this.currentContract = null
                this.volume = 1
                this.stopPrice = 0
                this.offset = 0
                this.action = ""
            },
            // changeLmtPrice() {
            //     switch (this.action) {
            //         case "BUY":
            //             this.limitPrice = this.stopPrice + this.offset
            //             break
            //         case "SELL":
            //             this.limitPrice = this.stopPrice - this.offset
            //             break
            //         default:
            //             this.limitPrice = 0
            //     }
                
            // }
		}
}
</script>