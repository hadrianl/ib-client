<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="fills"
    item-key="execution.execId"
    calculate-widths
    sort-by="time"
    sort-desc
    hide-default-footer
    class="elevation-1"
    >
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

export default {
    data() {
        return {
            headers : [
                {
                    text: 'time',
                    value: 'execution.time',
                    align: 'center',
                    sortable: true,
                },
                {
                    text: 'execId',
                    value: 'execution.execId',
                    align: 'center',
                    sortable: false,
                    divider: true,
                },
                {
                    text: 'contract',
                    value: 'contract',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'side',
                    value: 'execution.side',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'qty',
                    value: 'execution.shares',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'price',
                    value: 'execution.price',
                    align: 'center',
                },
                {
                    text: 'fee',
                    value: 'commissionReport.commission',
                    align: 'center',
                    divider: true,
                },
                {
                    text: 'orderId',
                    value: 'execution.orderId',
                    align: 'center',
                },
                {
                    text: 'permId',
                    value: 'execution.permId',
                    align: 'center',
                },
                {
                    text: 'account',
                    value: 'execution.acctNumber',
                    sortable: false,
                }

            ]
        }
    },
    props: {
			height: {
                type: String,
                defalut: "300"
			},
        },
    created() {

    },
    computed: {
        fills() {
            return this.$store.state.fillsList
        }
    },
    methods: {

    }
}
</script>
<style>

</style>