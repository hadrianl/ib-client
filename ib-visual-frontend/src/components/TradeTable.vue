<template>
    <Table :height="height" :columns="columns" :data="trades" :row-class-name="rowClassName">
        <template slot-scope="{ row }" slot="handle">
            <Button v-if="isDone(row.orderStatus.status)" 
            type="error" 
            size="small" 
            @click="cancelOrder(row.order)">Cancell</Button>
        </template>
    </Table>
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
            columns : [
                {title: 'permId',
                width: 120,
                fixed: 'left',
                sortable: true,
                sortType: 'desc',
                 render: (h, params) => {
                     return h('div', params.row.order.permId)
                 }
                },
                {title: 'c',
                //  width: 30,
                 align: 'left',
                 render: (h, params) => {
                     return h('div', params.row.order.clientId)
                 }
                },
                {title: 'orderId',
                //  width: 100,
                 align: 'left',
                 render: (h, params) => {
                     return h('div', params.row.order.orderId)
                 }
                },
                {title: 'symbol',
                // width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.contract.symbol + params.row.contract.lastTradeDateOrContractMonth.substr(2, 4))
                 }
                },
                {title: 'action',
                // width: 80,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.action)
                 }
                },
                {title: 'filled',
                // width: 70,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.filledQuantity)
                 }
                },
                {title: 'vol',
                // width: 70,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.totalQuantity)
                 }
                },
                {title: 'lmtPrice',
                // width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.lmtPrice)
                 }
                },
                {title: 'auxPrice',
                // width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.auxPrice)
                 }
                },
                {title: 'status',
                // width: 120,
                align: 'center',
                filters:[
                    {label: '有效订单',
                    value: 1},
                    {label: '运行中订单',
                    value: 2},
                    {label: '客户端订单',
                    value: 3},
                ],
                filterMultiple: false,
                filterMethod: (value, row) => {
                    switch(value){
                        case 1:
                            return ['Cancelled', 'ApiCancelled'].indexOf(row.orderStatus.status) == -1
                        case 2:
                            return ['Submitted', 'PreSubmitted'].indexOf(row.orderStatus.status) != -1
                        case 3:
                            return row.order.orderId > 0
                    }
                },
                filteredValue: [1],
                render: (h, params) => {
                     return h('div', params.row.orderStatus.status)
                 }
                },
                {title: 'orderRef',
                width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.orderRef)
                 }
                },
                {title: 'handle',
                 slot: 'handle',
                 width: 100,
                 align: 'center'
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
            return this.$store.state.tradesList
        }
    },
    mounted() {
        // var _this = this
        // this.$ibws.on('trades', function (ts) {
        //     console.log(ts)
        //     _this.$store.commit('initTrades', ts)
        // })
        
        // this.$ibws.on('trade', function (t) {
        //     console.log(t)
        //     _this.$store.commit('updateTrade', t) 
        // })

        // this.$ibws.send({'action': "get_all_trades"})
    },
    beforeDestroy: () => {
        // 实例销毁之前调用。在这一步，实例仍然完全可用。
        // Vue.$ibws.off('trades')
        // Vue.$ibws.off('trade')
	},
    methods: {
        isDone(status) {
            return ['Cancelled', 'ApiCancelled', 'Filled'].indexOf(status) == -1
        },
        cancelOrder(order) {
            this.$ibws.send({'action':'cancel_order', 'order': order})
        },
        rowClassName(row) {
            switch (row.orderStatus.status){
                case 'Filled':
                    return 'table-filled-row'
                case 'Submitted':
                    return 'table-submitted-row'
                case 'PreSubmitted':
                    return 'table-presubmitted-row'
                case 'Cancelled':
                    return 'table-cancelled-row'
                default:
                    return ''
            }
        }
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