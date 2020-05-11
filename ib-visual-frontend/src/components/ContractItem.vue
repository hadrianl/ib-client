<template>
    <v-autocomplete
    :value="currentItem"
    :items="itemsList"
    :search-input.sync="search"
    :success="hasContract"
    @input="selectItem"
    @click:clear="clearItem"
    color="white"
    hide-no-data
    item-text= "symbol"
    item-value="contract"
    label="Contract"
    placeholder="输入合约"
    prepend-icon="mdi-ios-search"
    chips
    small-chips
    deletable-chips
    dense
    outlined
    clearable
    hide-details="auto"
    return-object>
        <template v-slot:prepend>
            <v-icon
            :color="hasContract?'success':'error'"
            >{{hasContract?'mdi-text-box-check-outline':'mdi-text-box-remove-outline'}}</v-icon>
        </template>
    </v-autocomplete>
</template>
<script>
import {Contract} from '../plugins/datastructure.js'
const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    data() {
        return {
            search: null,
        }
    },
    computed: {
        currentItem() {
            const c = this.$store.state.currentContract

            if(!c) return null
            console.log(c)
            return  {'symbol': c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4),
                    'contract': c,}
        },
        hasContract() {
            return Boolean(this.$store.state.currentContract)
        },
        itemsList() {
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
        // var _this = this
        // this.$ibws.on('contract', function(c) {
        //     _this.$store.commit('addContract', c)
        // })
        this.$ibws.on('contract', c => this.$store.commit('addContract', c))

    },
    methods: {
        selectItem(item) {
            if(item){
                this.$store.commit('selectContract', item.contract)
            }

        },
        clearItem() {
            console.log('clearItem')
            this.$store.commit('clearContract')
        },


    },
    watch: {
        search(val) {
            var ret = patt.exec(val)
            if (ret) {
                let flag = true
                this.itemsList.forEach( c => {if(c.symbol === ret[0]) {flag = false}})
                    // function(c){
                    //     if (c.symbol === ret[0]){
                    //         flag = false
                    //     }
                    // })

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

