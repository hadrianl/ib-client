<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="trades"
    hide-default-footer
    class="elevation-1"
    >
        <template v-slot: item.handle="{ item }">
            <v-btn 
            v-if="isDone(item.status)"
            @click="cancelOrder(item.order)"
            color="error"
            small
            ></v-btn>
        </template>
    </v-data-table>
    

    <!-- <Table :height="height" :columns="columns" :data="trades" :row-class-name="rowClassName">
        <template slot-scope="{ row }" slot="handle">
            <Button v-if="isDone(row.orderStatus.status)" 
            type="error" 
            size="small" 
            @click="cancelOrder(row.order)">Cancell</Button>
        </template>
    </Table> -->
</template>

<script>
// import Vue from 'vue'

// function orderKey(orderId, permId, clientId) {
//     if (orderId <= 0) {
//         return String(permId)
//     }else{
//         return String(clientId) + String(orderId)
//     }
// }

// function is_same_key(n_trade, o_trade) {
//     var nKey = orderKey(n_trade.order.orderId, n_trade.order.permId, n_trade.order.clientId)
//     var oKey = orderKey(o_trade.order.orderId, o_trade.order.permId, o_trade.order.clientId)
    
//     return nKey == oKey
// }


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
                    sort: (a, b) => a-b
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
                    text: 'status',
                    value: 'status',
                    filterable: true,
                    align: 'center',
                    filter: (value, search, item) => {
                        let status = item.status
                        switch(value){
                            case 1:
                                return ['Cancelled', 'ApiCancelled'].indexOf(status) == -1
                            case 2:
                                return ['Submitted', 'PreSubmitted'].indexOf(status) != -1
                            case 3:
                                return item.order.orderId > 0
                        }
                    },
                },
                {
                    text: 'orderRef',
                    value: 'orderRef',
                },
                {
                    text: '',
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
            this.$store.state.tradesList.forEach(v => {
                trades.push({
                    permId: v.order.permId,
                    clientId: v.order.clientId,
                    orderId: v.order.orderId,
                    symbol: v.contract.symbol + v.contract.lastTradeDateOrContractMonth.substr(2, 4),
                    action: v.order.action,
                    filledQty: v.order.filledQuantity,
                    totalQty: v.order.totalQuantity,
                    lmtPrice: v.order.lmtPrice,
                    auxPrice: v.order.auxPrice,
                    status: v.orderStatus.status,
                    orderRef: v.order.orderRef,
                    order: v.order,
                })
            })
            return trades
        }
    },
    mounted() {

    },
    beforeDestroy: () => {

	},
    methods: {
        isDone(status) {
            return ['Cancelled', 'ApiCancelled', 'Filled'].indexOf(status) == -1
        },
        cancelOrder(order) {
            this.$ibws.send({'action':'cancel_order', 'order': order})
        },
        // rowClassName(row) {
        //     switch (row.orderStatus.status){
        //         case 'Filled':
        //             return 'table-filled-row'
        //         case 'Submitted':
        //             return 'table-submitted-row'
        //         case 'PreSubmitted':
        //             return 'table-presubmitted-row'
        //         case 'Cancelled':
        //             return 'table-cancelled-row'
        //         default:
        //             return ''
        //     }
        // }
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