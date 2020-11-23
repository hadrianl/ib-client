<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="trades"
    item-key="order.permId"
    :expanded.sync="expandedTrade"
    fixed-header
    disable-pagination
    calculate-widths
    single-expand
    show-expand
    sort-by="order.permId"
    sort-desc
    hide-default-footer
    class="elevation-1"
    >
        <template v-slot:expanded-item="{ headers, item }">
            <td v-for="f in item.fills" :key="f.execution.time" :colspan="headers.length">
                {{ f.execution.time.substr(0, 19) }}-----<strong>{{ f.execution.shares }}</strong>@<strong>{{ f.execution.price}}</strong> ${{ f.commissionReport.commission + f.commissionReport.currency}}[{{f.execution.execId}}]
            </td>
        </template>
        <template v-slot:item.operation="{ item }">
            <v-btn 
            v-if="!isDone(item.orderStatus.status)"
            @click="cancelOrder(item.order)"
            color="error"
            small
            >
            <v-tooltip v-if="item.order.parentId" top>
                <template v-slot:activator="{ on }">
                    <v-icon x-small dense left v-on="on">
                    mdi-format-list-bulleted-square
                    </v-icon>
                </template>
                <span>
                    parentID: {{item.order.parentId}}
                </span>
            </v-tooltip>  
            Cancel</v-btn>
        </template>
        
    </v-data-table>
</template>

<script>

export default {
    data() {
        return {
            expandedTrade: [],
            headers : [
                {
                    text: '', 
                    value: 'data-table-expand',
                    divider: true,
                },
                {
                    text: 'permId',
                    value: 'order.permId',
                    align: 'center',
                    sortable: true,
                    sort: (a, b) => a-b
                },
                {
                    text: 'c',
                    value: 'order.clientId',
                    align: 'center',
                },
                {
                    text: 'orderId',
                    value: 'order.orderId',
                    divider: true,
                    align: 'center',
                },
                {
                    text: 'symbol',
                    value: 'contract.localSymbol',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'action',
                    value: 'order.action',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'filled',
                    value: 'order.filledQuantity',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'remaining',
                    value: 'orderStatus.remaining',
                    align: 'center',
                    divider: true,
                    sortable: false,
                },
                {
                    text: 'lmtPrice',
                    value: 'order.lmtPrice',
                    align: 'center',
                },
                {
                    text: 'auxPrice',
                    value: 'order.auxPrice',
                    align: 'center',
                },
                {
                    text: 'orderType',
                    value: 'order.orderType',
                    align: 'center',
                },
                {
                    text: 'status',
                    value: 'orderStatus.status',
                    divider: true,
                },
                {
                    text: 'orderRef',
                    value: 'order.orderRef',
                    align: 'center',
                    sortable: false,
                },
                {
                    text: 'operation',
                    value: 'operation',
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
        trades() {
            return this.$store.getters.availableTradesList
        }
    },
    methods: {
        isDone(status) {
            return ['Cancelled', 'ApiCancelled', 'Filled'].includes(status)
        },
        cancelOrder(order) {
            this.$ibws.send({'action': 'cancel_order', 'order': order})
        },
    }
}
</script>
<style>

</style>