<template>
    <Table :columns="columns" :data="tradesArr" :row-class-name="rowClassName">
        <template slot-scope="{ row }" slot="handle">
            <Button v-if="done_status.indexOf(row.orderStatus.status) == -1" 
            type="error" 
            size="small" 
            @click="cancelOrder(row.order)">Cancell</Button>
        </template>
    </Table>
</template>

<script>
import Vue from 'vue'

function orderKey(orderId, permId, clientId) {
    if (orderId <= 0) {
        return String(permId)
    }else{
        return String(clientId) + String(orderId)
    }
}

function is_same_key(n_trade, o_trade) {
    var nKey = orderKey(n_trade.order.orderId, n_trade.order.permId, n_trade.order.clientId)
    var oKey = orderKey(o_trade.order.orderId, o_trade.order.permId, o_trade.order.clientId)
    
    return nKey == oKey
}


export default {
    data() {
        return {
            cancelled_status: ['Cancelled', 'ApiCancelled'],
            done_status: ['Cancelled', 'ApiCancelled', 'Filled'],
            tradesArr: [],
            columns : [
                {title: 'permId',
                width: 100,
                fixed: 'left',
                sortable: true,
                 render: (h, params) => {
                     return h('div', params.row.order.permId)
                 }
                },
                {title: 'c',
                 width: 30,
                 align: 'left',
                 render: (h, params) => {
                     return h('div', params.row.order.clientId)
                 }
                },
                {title: 'orderId',
                 width: 100,
                 align: 'left',
                 render: (h, params) => {
                     return h('div', params.row.order.orderId)
                 }
                },
                {title: 'conId',
                width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.contract.symbol + params.row.contract.lastTradeDateOrContractMonth.substr(2, 4))
                 }
                },
                {title: 'action',
                // key: 'order.action',
                width: 80,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.action)
                 }
                },
                {title: 'filled',
                // key: 'orderStatus.filled',
                width: 70,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.orderStatus.filled)
                 }
                },
                {title: 'vol',
                // key: 'order.totalQuantity',
                width: 70,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.totalQuantity)
                 }
                },
                {title: 'lmtPrice',
                // key: 'order.lmtPrice',
                width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.lmtPrice)
                 }
                },
                {title: 'auxPrice',
                // key: 'order.auxPrice',
                width: 100,
                align: 'left',
                render: (h, params) => {
                     return h('div', params.row.order.auxPrice)
                 }
                },
                {title: 'status',
                // key: 'orderStatus.status',
                width: 120,
                align: 'center',
                render: (h, params) => {
                     return h('div', params.row.orderStatus.status)
                 }
                },
                {title: 'orderRef',
                // key: 'order.orderRef',
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
			},
        },
    created() {

    },
    mounted() {
        var _this = this
        this.$ibws.on('trades', function (ts) {
            console.log(ts)
            _this.tradesArr = []
            for (let i in ts){
                var status = ts[i].orderStatus.status
                var is_cancelled = _this.cancelled_status.indexOf(status) != -1
                if (!is_cancelled) {
                    _this.tradesArr.unshift(ts[i])
                }
            }
        })
        
        this.$ibws.on('trade', function (t) {
            console.log(t)
            var status = t.orderStatus.status
            var is_cancelled = _this.cancelled_status.indexOf(status) != -1
            for (let i in _this.tradesArr){

                if (is_same_key(t, _this.tradesArr[i])){
                    if (is_cancelled){
                        _this.tradesArr.splice(i, 1)
                        return
                    }else{
                        console.log('set:', t)
                        _this.tradesArr.splice(i, 1, t)
                        return
                    }     
                }
            }


            _this.tradesArr.unshift(t)
            
        })

        this.$ibws.send({'action': "get_all_trades"})
    },
    beforeDestroy: () => {
        // 实例销毁之前调用。在这一步，实例仍然完全可用。
        Vue.$ibws.off('trades')
        Vue.$ibws.off('trade')
	},
    methods: {
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

    /* .ivu-table .table-presubmitted-row td{
        background-color: #187;
        color: #000;
    } */

</style>