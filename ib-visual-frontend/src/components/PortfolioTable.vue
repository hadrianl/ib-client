<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="portfolio"
    hide-default-footer
    class="elevation-1">
        <template v-slot:item.contract="{ item }">
            <v-tooltip bottom>
                <template v-slot:activator="{ on }">
                    <a v-on="on" @click.stop="$store.commit('addContract', item.contract);$store.commit('selectContract', item.contract)">{{ item.contract.localSymbol }}</a>
                </template>
                <span>
                    单击跳转到-> {{ item.contract.localSymbol }}<br>
                    ConId:{{ item.contract.conId }}<br>
                    Expire: {{ item.contract.lastTradeDateOrContractMonth}}<br>
                    Exchange: {{ item.contract.exchange}}<br>
                    Currency: {{item.contract.currency}}<br>
                    SecType: {{item.contract.secType}}
                </span>
            </v-tooltip>
        </template> 
    </v-data-table>

</template>
<script>
// import Vue from 'vue'
export default {
     data() {
        return {
            headers : [
                    {
                        text: 'contract',
                        value: 'contract',
                        sortable: true,
                    },
                    {
                        text: 'position',
                        value: 'position'
                    },
                    {
                        text: 'marketPrice',
                        value: 'marketPrice',
                    },
                    {
                        text: 'marketValue',
                        value: 'marketValue',
                    },
                    {
                        text: 'averageCost',
                        value: 'averageCost',
                    },
                    {
                        text: 'unrealizedPNL',
                        value: 'unrealizedPNL',
                    },
                    {
                        text: 'realizedPNL',
                        value: 'realizedPNL',
                    },
                    {
                        text: 'account',
                        value: 'account',
                    }]
                }
            },
     props: {
			height: {
                type: String,
                defalut: "200",
			},
        },
    computed: {
        portfolio() {
            return this.$store.state.portfolioList
        }
    },
    methods: {
        rowClassName(row) {
            switch (true){
                case row.position > 0:
                    return 'table-positive-row'
                case row.position < 0:
                    return 'table-negative-row'
                default:
                    return 'table-normal-row'
            }
        }
    }
        }
</script>
<style>

</style>