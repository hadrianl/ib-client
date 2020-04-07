<template>
    <div>
        <div ref="barChart" class="ChartContainer" id="bar-chart"></div>
        <RadioGroup v-model="action" type="button">
            <Radio label="BUY">BUY</Radio>
            <Radio label="SELL">SELL</Radio>
        </RadioGroup>
        <InputNumber v-model="volume" :min="1" style="width: auto"></InputNumber>
        <InputNumber v-model="offset" :min="0" style="width: auto"></InputNumber>
    </div>
    
</template>
<script>
import { createChart, LineStyle } from 'lightweight-charts'
import {Order} from '../plugins/datastructure.js'
import {orderKey} from '../store/store.js'
import Vue from 'vue'
export default {
    // const chart = createChart(this.$refs.barChart, {width: 1200, height: 500})
    props: {

    },
    computed:{
        contract() {
            return this.$store.state.currentContract
        }
    },
    data() {
        return {
            chart: null,
            ohlcSeries: null,
            volSeries: null,
            orderLines: {},
            action: "",
            volume: 1,
            offset: 0,
        }
    },
    mounted() {
        this.chart = createChart(this.$refs.barChart, {width: 1300, height: 500})
        this.ohlcSeries = this.chart.addCandlestickSeries()
        this.volSeries = this.chart.addHistogramSeries({base: 0, overlay: true})
        this.chart.applyOptions({
            crosshair: {
                mode: 0
            }
        })
        this.ohlcSeries.applyOptions({
            upColor: '#6495ED',
            downColor: '#FF6347',
            borderVisible: false,
            wickVisible: true,
            borderColor: '#000000',
            wickColor: '#000000',
            borderUpColor: '#4682B4',
            borderDownColor: '#A52A2A',
            wickUpColor: "#4682B4",
            wickDownColor: "#A52A2A",
            scaleMargins: {
                top: 0.1,
                bottom: 0.3
            }
        })
        this.volSeries.applyOptions({
            // base: 0,
            // overlay: true,
            scaleMargins: {
                top: 0.6,
                bottom: 0.02
            }
        })
        var _this = this
        this.chart.subscribeClick(function(param) {
            console.log(param)
            // console.log(_this.ohlcSeries.coordinateToPrice(param.point.y))
            const price = _this.ohlcSeries.coordinateToPrice(param.point.y)
            // console.log(_this.ohlcSeries)
            const lastPrice = _this.ohlcSeries.series().bars().last().value[3]
            console.log(price, lastPrice, _this.action, _this.contract)
            switch(true) {
                case _this.contract && price > lastPrice && _this.action == 'BUY':
                    {
                        let order = new Order()
                        order.outsideRth = true
                        order.orderType = 'STP LMT'
                        order.lmtPrice = parseInt(price + _this.offset)
                        order.auxPrice = parseInt(price)
                        order.action = 'BUY'
                        order.totalQuantity = _this.volume
                        console.log({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        _this.$ibws.send({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        break
                    }    
                case _this.contract && price < lastPrice && _this.action == 'BUY':
                    {
                        let order = new Order()
                        order.outsideRth = true
                        order.orderType = 'LMT'
                        order.lmtPrice = parseInt(price)
                        order.action = 'BUY'
                        order.totalQuantity = _this.volume
                        console.log({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        _this.$ibws.send({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        break
                    }
                case _this.contract && price < lastPrice && _this.action == 'SELL':
                    {
                        let order = new Order()
                        order.outsideRth = true
                        order.orderType = 'STP LMT'
                        order.lmtPrice = parseInt(price - _this.offset)
                        order.auxPrice = parseInt(price)
                        order.action = 'SELL'
                        order.totalQuantity = _this.volume
                        console.log({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        _this.$ibws.send({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        break
                    }
                    
                case _this.contract && price > lastPrice && _this.action == 'SELL':
                    {
                        let order = new Order()
                        order.outsideRth = true
                        order.orderType = 'LMT'
                        order.lmtPrice = parseInt(price)
                        order.action = 'SELL'
                        order.totalQuantity = _this.volume
                        console.log({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        _this.$ibws.send({'action': 'place_order', 'contract': _this.contract, 'order': order})
                        break
                    }
                default:
                    {
                        _this.$Notice.error({
                            title: 'Order Failed!',
                            desc: "请先选择合约和开单方向",
                            duration: 5
                        })
                    }
               
            }

            _this.action = ""



            // _this.ohlcSeries.createPriceLine({
            //                     price: price,
            //                     color: 'green',
            //                     lineWidth: 2,
            //                     lineStyle: LineStyle.Dotted,
            //                     axisLabelVisible: true,
            //                 })
            })

        this.$ibws.on('trade', this.addOrderLine)

        
        this.$ibws.on('bars', function(bs) {
            let volArr = []
            bs.forEach((element, index) => {
                let t = new Date(element.time).getTime() / 1000
                bs[index].time = t
                volArr.push({'time': t, 'value': element.volume})
            })
            _this.ohlcSeries.setData(bs)
            _this.volSeries.setData(volArr)
            // _this.$store.state.tradesList.forEach(t => _this.addOrderLine(t))
            _this.$store.state.tradesList.forEach(t => console.log(t))
        })

        this.$ibws.on('bar', function(b) {
            let t = new Date(b.time).getTime() / 1000
            b.time = t
            _this.ohlcSeries.update(b)
            _this.volSeries.update({'time': t, 'value': b.volume})
        })

        // this.$ibws.on('trade', function(t) {

        // })
        if (this.contract){
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract})
        }

    },
    methods: {
        addOrderLine(t) {
            const key = orderKey(t.order.orderId, t.order.permId, t.order.clientId)
            // remove the line when the order is done
            if(['Cancelled', 'ApiCancelled', 'Filled'].indexOf(t.orderStatus.status) != -1 && this.orderLines[key]){
                this.ohlcSeries.removePriceLine(this.orderLines[key])
                delete this.orderLines[key]
                return
            }

            // check contract
            if (t.contract.conId != this.contract.conId){
                return
            }

            let line_option = {}
            switch(t.order.orderType){
            case 'LMT':
                {
                    line_option = {
                    price: t.order.lmtPrice,
                    color: t.order.action == 'BUY'?'red':'green',
                    lineWidth: 2,
                    lineStyle: LineStyle.Dotted,
                    axisLabelVisible: true,
                    }
                    break
                }
                
            case 'STP LMT':
                {
                    let isPreSubmitted = t.orderStatus.status == 'PreSubmitted'
                    line_option = {
                        price: isPreSubmitted?t.order.auxPrice:t.order.lmtPrice,
                        color: t.order.action == 'BUY'?'red':'green',
                        lineWidth: 2,
                        lineStyle: isPreSubmitted?LineStyle.Dashed:LineStyle.Dotted,
                        axisLabelVisible: true,
                    }
                    break
                }
                
                }

            if (this.orderLines[key]){
                let line = this.orderLines[key]
                line.applyOptions(line_option)
            }else{
                if(line_option) {
                    let line = this.ohlcSeries.createPriceLine(line)
                    this.orderLines[key] = line
                    }
            }
        }
    },
    destroyed: () => {
        // 实例销毁之前调用。在这一步，实例仍然完全可用。
        console.log(this)
        Vue.$ibws.send({'action': 'unsub_klines'})
        Vue.$ibws.off('bars')
        Vue.$ibws.off('bar')
	},


}
</script>