<template>
    <div>
        <v-autocomplete
        :items="contractsList"
        :search-input.sync="search"
        @input="selectContract"
        @clear="clearContract"
        color="white"
        hide-no-data
        item-text= "symbol"
        item-value="contract"
        label="Contract"
        placeholder="输入合约"
        prepend-icon="mdi-ios-search"
        chips
        small-chips
        outlined
        clearable
        return-object
      ></v-autocomplete>

    <!-- <AutoComplete clearable	
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
    <Alert v-if="contract" type="success" show-icon>ConId：{{contract.conId}}</Alert> -->
    </div>
</template>
<script>
import {Contract} from '../plugins/datastructure.js'
const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    data() {
        return {
            condName: "",
            // contractsList: [],
        }
    },
    computed: {
        contract() {
            return this.$store.state.currentContract
        },
        contractsList() {
            let cl = []
            this.$store.state.contractsList.forEach(c => {
                cl.push({
                    'symbol': c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4),
                    'contract': c,
                })
            })
            return cl
        }
    },
    mounted() {
        var _this = this
        this.$ibws.on('contract', function(c) {
            _this.$store.commit('addContract', c)
        })
    },
    methods: {
        selectContract(contract) {
            this.$store.commit('selectContract', contract)

            // this.$ibws.send({'action': 'sub_klines','contract': contract})
        },
        clearContract() {
            this.$store.commit('clearContract')
        },
    },
    watch: {
        search(val) {
            var ret = patt.exec(val)
            if (ret) {
                let flag = true
                this.contractsList.forEach(function(c){
                if (c.symbol === ret[0]){
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
        }
    }
}
</script>

