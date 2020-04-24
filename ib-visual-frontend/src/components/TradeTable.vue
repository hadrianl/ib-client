<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="trades"
    sort-by="permId"
    hide-default-footer
    class="elevation-1"
    >
        <template v-slot:item.handle="{ item }">
            <v-btn 
            v-if="isDone(item.status)"
            @click="cancelOrder(item.order)"
            color="error"
            small
            >Cancel</v-btn>
        </template>
    </v-data-table>
</template>

<script>

export default {
    data() {
        return {
            // cancelled_status: ['Cancelled', 'ApiCancelled'],
            // done_status: ['Cancelled', 'ApiCancelled', 'Filled'],
            // tradesArr: [],
            headers : [
                {
                    text: 'permId',
                    value: 'permId',
                    sortable: true,
                    sort: (a, b) => b-a
                },
                {
                    text: 'c',
                    value: 'clientId',
                },
                {
                    text: 'orderId',
                    value: 'orderId',
                    align: 'start',
                },
                {
                    text: 'symbol',
                    value: 'symbol',
                },
                {
                    text: 'action',
                    value: 'action',
                },
                {
                    text: 'filledQty',
                    value: 'filledQty',
                },
                {
                    text: 'totalQty',
                    value: 'totalQty',
                },
                {
                    text: 'lmtPrice',
                    value: 'lmtPrice',   
                },
                {
                    text: 'auxPrice',
                    value: 'auxPrice',
                },
                {
                    text: 'orderType',
                    value: 'orderType',
                },
                {
                    text: 'status',
                    value: 'status',
                    filterable: true,
                    align: 'center',
                    filter: (value, search, item) => {
                        console.log(value)
                        console.log(search)
                        console.log(item)
                        return true
                        // const status = item.status
                        // switch(value){
                        //     case 1:
                        //         return ['Cancelled', 'ApiCancelled'].indexOf(status) == -1
                        //     case 2:
                        //         return ['Submitted', 'PreSubmitted'].indexOf(status) != -1
                        //     case 3:
                        //         return item.order.orderId > 0
                        // }
                    },
                },
                {
                    text: 'orderRef',
                    value: 'orderRef',
                },
                {
                    text: 'handle',
                    value: 'handle',
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
            let trades = []
            this.$store.getters.availableTradesList.forEach(v => {
                trades.push({
                    permId: v.order.permId,
                    clientId: v.order.clientId,
                    orderId: v.order.orderId,
                    symbol: v.contract.symbol + v.contract.lastTradeDateOrContractMonth.substr(2, 4),
                    action: v.order.action,
                    filledQty: v.order.filledQuantity == Number.MAX_VALUE?0:v.order.filledQuantity,
                    totalQty: v.order.totalQuantity,
                    lmtPrice: v.order.lmtPrice,
                    auxPrice: v.order.auxPrice,
                    orderType: v.order.orderType,
                    status: v.orderStatus.status,
                    orderRef: v.order.orderRef,
                    order: v.order,
                })
            })
            console.log(trades)
            return trades
        }
    },
    mounted() {

    },
    beforeDestroy() {

	},
    methods: {
        isDone(status) {
            return ['Cancelled', 'ApiCancelled', 'Filled'].indexOf(status) == -1
        },
        cancelOrder(order) {
            this.$ibws.send({'action': 'cancel_order', 'order': order})
        },
    }
}
</script>
<style>
    .ivu-table .table-filled-row td{
        background-color: #ff6600;
        color: #000;
    }
    .ivu-table .table-submitted-row td{
        background-color: #2db7f5;
        color: #000;
    }
    .ivu-table .table-presubmitted-row td{
        background-color: #187;
        color: #000;
    }

    .ivu-table .table-cancelled-row td{
        background-color: #DCDCDC;
        color: #000;
    }

</style>