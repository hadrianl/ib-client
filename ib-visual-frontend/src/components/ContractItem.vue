<template>
    <!-- <div> -->
        <v-autocomplete
        :value="contract"
        :items="contractsList"
        :search-input.sync="search"
        :success="contract"
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
        dense
        outlined
        clearable
        return-object>
            <template v-slot:prepend>
                <v-icon>mdi-place</v-icon>
            </template>
        </v-autocomplete>

</template>
<script>
import {Contract} from '../plugins/datastructure.js'
const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    data() {
        return {
            condName: "",
            search: null,
            // contractsList: [],
        }
    },
    computed: {
        contract() {
            return this.$store.state.currentContract
        },
        hasContract() {
            console.log(Boolean(this.$store.state.currentContract))
            return Boolean(this.$store.state.currentContract)
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
        selectContract(value) {
            console.log(value)
            let oldCon = this.contract
            if(value){
                this.$store.commit('selectContract', value.contract)
                this.$emit('changeContract', {'old': oldCon, 'new': value.contract})
            }
            

            // this.$ibws.send({'action': 'sub_klines','contract': contract})
        },
        clearContract() {
            this.$store.commit('clearContract')
        },


    },
    watch: {
        search(val) {
            console.log(val)
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

