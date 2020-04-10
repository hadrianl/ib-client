<template>
    <div>
        <div ref="barChart" class="ChartContainer" id="bar-chart"></div>
        <RadioGroup v-model="action" type="button">
            <Radio label="BUY">BUY</Radio>
            <Radio label="SELL">SELL</Radio>
        </RadioGroup>
        <InputNumber v-model="volume" :min="1" style="width: auto"></InputNumber>
        <InputNumber v-model="offset" :min="0" style="width: auto"></InputNumber>
        <!-- <Button type="info" @click="init">初始化</Button> -->
    </div>
    
</template>
<script>
import { createChart, LineStyle} from 'lightweight-charts'
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
        },
        trades() {
            return this.$store.getters.currenTradesList
        },
        fills() {
            return this.$store.getters.currentFillsList
        },
        markers() {
            let arr = []
            this.fills.forEach(f => arr.push({
                        time: new Date(f.execution.time).getTime() / 1000 + 28800,
                        position: f.execution.side==='BOT'?'belowBar':'aboveBar',
                        shape: f.execution.side==='BOT'?'arrowUp':'arrowDown',
                        color: f.execution.side==='BOT'?'red':'green',
                        id: f.execution.permId,
                    }))
            arr.sort((a, b)=>a.time - b.time)
            return arr
        }
    },
    data() {
        return {
            chart: null,
            ohlcSeries: null,
            volSeries: null,
            maSeries: null,
            orderLines: {},
            tradeMarkers: {},
            action: "",
            volume: 1,
            offset: 0,
        }
    },
    mounted() {
        const chartOptions = {
            width: 1300, 
            height: 500,
            timeScale: {
                rightOffset: 10,
                // barSpacing: number;
                fixLeftEdge: true,
                // lockVisibleTimeRangeOnResize: true,
                rightBarStaysOnScroll: true,
                // borderVisible: boolean;
                // borderColor: string;
                // visible: boolean;
                timeVisible: true,
                secondsVisible: true
            }
        }
        this.chart = createChart(this.$refs.barChart, chartOptions)
        this.ohlcSeries = this.chart.addCandlestickSeries()
        this.volSeries = this.chart.addHistogramSeries({base: 0, overlay: true})
        // this.maSeries = this.chart.addLineSeries()
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
            scaleMargins: {
                top: 0.6,
                bottom: 0.02
            }
        })

        // var _this = this
        this.chart.subscribeClick(this.onChartClick)
        // this.chart.subscribeVisibleTimeRangeChange(this.onTimeRangeChange)

        this.$ibws.on('trade', this.handleTrade)

        this.$ibws.on('bars', this.handleBars)

        this.$ibws.on('bar', this.handleBar)

        this.$ibws.once('bars', this.initAddition)

        if (this.contract){
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract})
        }
        console.log(this.markers)
        console.log(this)
    },
    methods: {
        handleTrade(t) {
            // check contract
            if (t.contract.conId != this.contract.conId){
                return
            }

            const key = orderKey(t.order.orderId, t.order.permId, t.order.clientId)
            // remove the line when the order is done
            if(['Cancelled', 'ApiCancelled', 'Filled'].indexOf(t.orderStatus.status) != -1){
                if(this.orderLines[key]){
                    this.ohlcSeries.removePriceLine(this.orderLines[key])
                    delete this.orderLines[key]
                }
                
                if(t.orderStatus.status == 'Filled'){
                    this.ohlcSeries.setMarkers(this.markers)
                }

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
            }else if(line_option) {
                console.log(line_option)
                let line = this.ohlcSeries.createPriceLine(line_option)
                this.orderLines[key] = line
                }
        },
        handleBars(bars) {
            let volArr = []
            // let maArr = []
            bars.forEach((element, index) => {
                let t = new Date(element.time).getTime() / 1000 + 28800
                bars[index].time = t
                volArr.push({'time': t, 'value': element.volume})
                // if(index < 5){
                //     maArr.push({'time': t, 'value': '-'})
                // }else{
                //     let sum = 0
                //     arr.slice(index - 5, index).forEach(b => sum += b.close)
                //     maArr.push({'time': t, 'value':sum / 5})
                // }
            })
            this.ohlcSeries.setData(bars)
            this.volSeries.setData(volArr)
            // this.maSeries.setData(maArr)
            console.log(this.ohlcSeries)
            // this.trades.forEach(t => this.handleTrade(t))
        },
        handleBar(bar) {
            const t = new Date(bar.time).getTime() / 1000 + 28800
            bar.time = t
            this.ohlcSeries.update(bar)
            this.volSeries.update({'time': t, 'value': bar.volume})
            // let sum = 0
            // let size = this.ohlcSeries.series().data().size()
            // for(let i = 5;i > 0; i--){
            //     console.log(this.ohlcSeries.series().dataAt(size - i))
            //     sum += this.ohlcSeries.series().dataAt(size - i).close
            // }
            // this.maSeries.update({'time': t, 'value': sum / 5})
        },
        onChartClick(param) {
            const price = this.ohlcSeries.coordinateToPrice(param.point.y)
            const lastPrice = this.ohlcSeries.series().bars().last().value[3]
            switch(true) {
                case this.contract && price > lastPrice && this.action == 'BUY':
                    {
                        this.sendOrder('STP LMT', price, 'BUY')
                        break
                    }    
                case this.contract && price < lastPrice && this.action == 'BUY':
                    {
                        this.sendOrder('LMT', price, 'BUY')
                        break
                    }
                case this.contract && price < lastPrice && this.action == 'SELL':
                    {
                        this.sendOrder('STP LMT', price, 'SELL')
                        break
                    }
                    
                case this.contract && price > lastPrice && this.action == 'SELL':
                    {
                        this.sendOrder('LMT', price, 'SELL')
                        break
                    }
                default:
                    {
                        this.$Notice.error({
                            title: 'Order Failed!',
                            desc: "请先选择合约和开单方向",
                            duration: 5
                        })
                    }
               
            }

            this.action = ""
        },
        onTimeRangeChange(param) {
            // console.log(param.from)
            // console.log(param.to)
            // this.$ibws.once('bars_', )
            // this.$ibws.send({'action': 'get_klines', 'contract': this.contract, 'from': param.from, 'to': param.to})
            setTimeout(function(){
                console.log(param.from)
                console.log(param.to)
            }, 10000)
        },
        sendOrder(orderType, price, action) {
            // if no action , notice error
            if(!(this.contract && action)) {
                return
            }

            let order = new Order()
            order.outsideRth = true
            order.orderType = orderType
            order.action = action
            order.totalQuantity = this.volume

            switch(orderType) {
                case 'LMT':
                    {
                        order.lmtPrice = parseInt(price)
                        break
                    }
                    
                case 'STP LMT':
                    {
                        let offset = action == 'BUY'?this.offset:-this.offset
                        order.lmtPrice = parseInt(price)
                        order.auxPrice = order.lmtPrice + offset
                        break
                    }
                default:
                    return
            }
                 
            console.log({'action': 'place_order', 'contract': this.contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': this.contract, 'order': order})
        },
        initAddition() {
            this.trades.forEach(t => this.handleTrade(t))

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