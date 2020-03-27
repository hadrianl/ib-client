<template>
    <div>
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
    </div>
</template>
<script>
import {Contract} from '../plugins/datastructure.js'
const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    data() {
        return {
            condName: "",
            currentContract: null,
        }
    },
    props:{
        contractsList: Array
    },
    mounted() {
        // var _this = this
        // this.$ibws.on('contract', function(c) {
        //     var flag = true
        //     _this.contractsList.forEach(element => {
        //         if (element.conId === c.conId){
        //             flag = false
        //         }
        //     })
        //     if (flag){
        //         _this.contractsList.push(c)
        //     }
        // })
    },
    methods: {
        selectContract(item) {
            var contract = null
            this.contractsList.forEach(function(c){
                if ((c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4)) === item){
                    contract = c
                }
            })
            this.currentContract = contract
        },
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
        clearContract() {
            this.currentContract = null
        },
    }
}
</script>

