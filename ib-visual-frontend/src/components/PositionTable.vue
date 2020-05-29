<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="positions"
    fixed-header
    disable-pagination
    hide-default-footer
    class="elevation-1">
        <template v-slot:item.contract="{ item }">
            <v-tooltip right>
                <template v-slot:activator="{ on }">
                    <a v-on="on" @click.stop="$store.commit('addContract', item.contract);$store.commit('selectContract', item.contract)">{{ item.contract.localSymbol }}</a>
                </template>
                <h1 class='blue--text'>{{ item.contract.localSymbol }}</h1>
                <ul>
                    <li>ConId:{{ item.contract.conId }}</li>
                    <li>Expire: {{ item.contract.lastTradeDateOrContractMonth || "---" }}</li>
                    <li>Exchange: {{ item.contract.exchange}}</li>
                    <li>Currency: {{item.contract.currency}}</li>
                    <li>SecType: {{item.contract.secType}}</li>
                </ul>
                <p class='green--text'>Click to Select Contract!</p>
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
                        sortable: false,
                    },
                    {
                        text: 'position',
                        value: 'position',
                        sortable: false,
                    },
                    {
                        text: 'avgCost',
                        value: 'avgCost',
                    },
                    {
                        text: 'account',
                        value: 'account',
                        sortable: false,
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
        positions() {
            return this.$store.state.positionsList
        }
    },
    methods: {

    }
        }
</script>
<style>

</style>