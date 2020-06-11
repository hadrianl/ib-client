<template>
    <v-autocomplete
    v-model="currentItem"
    :items="itemsList"
    :search-input.sync="search"
    :success="hasContract"
    @click:clear="clearItem"
    color="white"
    hide-no-data
    item-text= "symbol"
    item-value="contract"
    label="Contract"
    :placeholder="$t('placeHolder.contractInput')"
    prepend-icon="mdi-ios-search"
    chips
    small-chips
    dense
    outlined
    clearable
    hide-details="auto"
    return-object>
        <template v-slot:prepend>
            <v-icon
            :color="hasContract?'success':'error'"
            >{{hasContract?'mdi-text-box-check-outline':'mdi-text-box-remove-outline'}}
            </v-icon>
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
        currentItem: {
            get () {
                const c = this.$store.state.currentContract

                if(!c) return null
                return  {'symbol': c.symbol + c.lastTradeDateOrContractMonth.substr(2, 4),
                        'contract': c,}
            },
            set (item) {
                if(item){
                    this.$store.commit('selectContract', item.contract)
                    this.$emit('select-contract', item.contract)
                }
            }
            
        },
        hasContract() {
            return !!this.$store.state.currentContract
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
        this.$ibws.on('contract', c => this.$store.commit('addContract', c))

    },
    methods: {
        clearItem() {
            this.$store.commit('clearContract')
            this.$emit('clear-contract')
        },


    },
    watch: {
        search(val) {
            let ret = patt.exec(val)
            if (ret) {
                let flag = true
                this.itemsList.forEach( c => {if(c.symbol === ret[0]) {flag = false}})

                if (flag){
                    let c = new Contract()
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

