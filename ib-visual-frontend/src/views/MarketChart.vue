<template>
    <v-container fluid class='mt-1 pt-1'>
        <v-card ref="barCard" :color="colors.background">
            <v-toolbar dense flat :color="colors.background">
                <v-radio-group v-model="barSize" dense mandatory dark hide-details row >
                    <v-radio value="1 min"   label="1 min"></v-radio>
                    <v-radio value="3 mins"  label="3 mins"></v-radio>
                    <v-radio value="5 mins"  label="5 mins"></v-radio>
                    <v-radio value="10 mins" label="10 mins"></v-radio>
                    <v-radio value="15 mins" label="15 mins"></v-radio>
                </v-radio-group>
                <v-spacer></v-spacer>
                <Predict :get_datas="get_datas"></Predict>
                <v-switch v-model="isTrail" :label="$t('button.trail')" dark dense hide-details></v-switch>
                <v-btn-toggle v-model="action" rounded dense class='mx-5'>
                    <v-btn value="BUY" color="red">{{$t('button.buy')}}</v-btn>
                    <v-btn value="SELL" color="green">{{$t('button.sell')}}</v-btn>
                </v-btn-toggle>
                <v-text-field 
                v-model.number="volume" 
                label="volume" 
                type="number" 
                dark
                :rules="volRules"
                dense
                outlined
                style="max-width: 80px"
                hide-details>
                </v-text-field>
                <v-text-field 
                v-model.number="offset" 
                label="offset" 
                type="number" 
                dark
                outlined 
                dense
                style="max-width: 100px"
                hide-details>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-collapse-up':'mdi-arrow-collapse-down':''}}</v-icon>
                    </template>
                </v-text-field>
            </v-toolbar>
            <v-responsive :aspect-ratio="16/9">
                <v-card-text v-resize="onResize">
                    <div ref="barChart" class="ChartContainer" id="bar-chart" 
                    @contextmenu.prevent="showMenu"
                    @mousedown="chart.subscribeVisibleTimeRangeChange(onTimeRangeChange)"
                    @mouseup="chart.unsubscribeVisibleTimeRangeChange(onTimeRangeChange)">
                        <v-menu
                            v-model="menu.isShow"
                            :position-x="menu.x"
                            :position-y="menu.y"
                            min-width="200"
                            absolute
                            offset-y
                            >
                            <v-list>
                                <v-list-item @click="cancelAll()">
                                    <v-list-item-title>{{$t('button.cancelAllOrders')}}</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                        <Legend :legend_bar="legend_bar" :legend_ma="legend_ma"></Legend>
                        <v-btn
                        id="forefront"
                        absolute
                        dark
                        fab
                        bottom
                        left
                        color="pink"
                        @click="gotoForefront"
                        >
                        <v-icon>mdi-menu-right</v-icon>
                        </v-btn>
                    </div>
                </v-card-text>
            </v-responsive>
        </v-card>
    </v-container>
    

</template>
<script>
import { createChart, LineStyle } from 'lightweight-charts'
import {Order} from '../plugins/datastructure.js'
import {orderKey} from '../store/store.js'
import Legend from '../components/charts/Legend.vue'
import Predict from '../components/PredictStock.vue'

export default {
    components: {
        Legend,
        Predict,
    },
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
                        time: f.time - 60,
                        position: f.execution.side==='BOT'?'belowBar':'aboveBar',
                        shape: f.execution.side==='BOT'?'arrowUp':'arrowDown',
                        color: f.execution.side==='BOT'?'red':'green',
                        id: f.execution.permId,
                        size: 0.1,
                    }))
            arr.sort((a, b)=>a.time - b.time)
            return arr
        }
    },
    data() {
        return {
            bars: [],
            chart: null,
            ohlcSeries: null,
            volSeries: null,
            maSeries: {5: null, 10: null, 30: null, 60: null},
            orderLines: {},
            tradeMarkers: {},
            barSize: "1 min",
            action: "",
            volume: 1,
            offset: 0,
            isTrail: false,
            legend_bar: {time: NaN, open: NaN, high: NaN, low: NaN, close: NaN, volume: NaN},
            legend_ma: {5: NaN, 10: NaN, 30: NaN, 60: NaN},
            volRules: [
                    v => v > 0,
                ],
            menu: {
                isShow: false,
                x: NaN,
                y: NaN,
            },
            colors: {
                background: '#000000',
                text: "#FFFFFF",
                tool: "#FFFFFF",
            },
        }
    },
    mounted() {
        const chartOptions = {
            width: this.$refs.barChart.clientWidth, 
            height: window.innerHeight * 0.7,
            layout: {
                backgroundColor: this.colors.background,
                textColor: this.colors.text,
            },
            grid: {
                vertLines: {
                    color: "#D8BFD8",
                    style: LineStyle.SparseDotted,
                },
                horzLines: {
                    color: "#D8BFD8",
                    style: LineStyle.SparseDotted,
                }
            },
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
            },
            crosshair: {
                mode: 0
            },
            localization: {
                locale: 'zh-Hans-CN'
            },
        }
        const ohlcOptions = {
            upColor: '#FF0000',
            downColor: '#00FFFF',
            borderVisible: false,
            wickVisible: true,
            // borderColor: '#000000',
            wickColor: '#FFFFFF',
            // borderUpColor: '#4682B4',
            // borderDownColor: '#A52A2A',
            // wickUpColor: "#4682B4",
            // wickDownColor: "#A52A2A",
            scaleMargins: {
                top: 0.1,
                bottom: 0.3
            }
        }
        const volOptions = {
            base: 0, 
            overlay: true,
            color: '#6495ED',
            scaleMargins: {
                top: 0.6,
                bottom: 0.02
            }
        }
        this.chart = createChart(this.$refs.barChart, chartOptions)
        this.ohlcSeries = this.chart.addCandlestickSeries(ohlcOptions)
        this.volSeries = this.chart.addHistogramSeries(volOptions)

        let colors = {5: '#DC143C', 10: '#FFC125', 30: '#C0FF3E', 60: '#97FFFF'}

        for(let key in this.maSeries){
            this.maSeries[key] = this.chart.addLineSeries({
                priceLineVisible: false, 
                lastValueVisible: false, 
                lineWidth: 1, 
                color: colors[key],
                })
        }

        this.chart.subscribeClick(this.onChartClick)
        this.chart.subscribeCrosshairMove(this.onCrosshairMove)

        this.$ibws.on('trade', this.handleTrade)

        this.$ibws.on('bars', this.handleBars)

        this.$ibws.on('bar', this.handleBar)

        this.$ibws.once('bars', this.initAddition)

        if (this.contract){
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract})
        }
        console.log(this)
        console.log(this.ohlcSeries)
    },
    watch: {
        contract(newCon, oldCon) {
            if (oldCon) {
                this.$ibws.send({'action': 'unsub_klines','contract': oldCon, 'barSize': this.barSize})
            }

            this.$ibws.once('bars', this.initAddition)
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract, 'barSize': this.barSize})
        },
        barSize(newSize, oldSize) {
            this.$ibws.send({'action': 'unsub_klines','contract': this.contract, 'barSize': oldSize})
            this.$ibws.once('bars', this.initAddition)
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract, 'barSize': newSize})
        },
        action(value) {
            console.log(this.chart.options().crosshair.horzLine.labelBackgroundColor)
            switch(value) {
                case 'BUY':
                    this.chart.applyOptions({
                        crosshair: {
                            horzLine: {
                                color: 'red',
                                width: 2,
                                style: 0,
                                labelBackgroundColor: 'red',
                            }
                        }
                        })
                        break
                case 'SELL':
                    this.chart.applyOptions({
                        crosshair: {
                            horzLine: {
                                color: 'green',
                                width: 2,
                                style: 0,
                                labelBackgroundColor: 'green',
                            }
                        }
                    })
                    break
                default:
                    this.chart.applyOptions({
                        crosshair: {
                            horzLine: {
                                color: '#758696',
                                width: 1,
                                style: 3,
                                labelBackgroundColor: '#4c525e',
                            }
                        }
                    })
            }
        }
    },
    methods: {
        showMenu(e) {
            e.preventDefault()
            this.menu.isShow = false
            this.menu.x = e.clientX
            this.menu.y = e.clientY
            this.$nextTick(() => {
                this.menu.isShow = true
                })
        },
        cancelAll() {
            this.$ibws.send({'action': 'cancel_all'})
        },
        handleTrade({contract, order, orderStatus}) {
            // check contract
            if (contract.conId != this.contract.conId){
                return
            }

            const key = orderKey(order)
            // remove the line when the order is done
            if(['Cancelled', 'ApiCancelled', 'Filled'].indexOf(orderStatus.status) != -1){
                if(this.orderLines[key]){
                    this.ohlcSeries.removePriceLine(this.orderLines[key])
                    delete this.orderLines[key]
                }
                
                if(orderStatus.status == 'Filled'){
                    this.ohlcSeries.setMarkers(this.markers)
                }

                return
            }

      
            let line_option = {}
            switch(order.orderType){
            case 'LMT':
                {
                    line_option = {
                    price: order.lmtPrice,
                    color: order.action == 'BUY'?'red':'green',
                    lineWidth: 2,
                    lineStyle: LineStyle.Dotted,
                    axisLabelVisible: true,
                    }
                    break
                }
                
            case 'STP LMT': case 'LIT': case 'STP':
                {
                    let isPreSubmitted = orderStatus.status == 'PreSubmitted'
                    line_option = {
                        price: isPreSubmitted?order.auxPrice:order.lmtPrice,
                        color: order.action == 'BUY'?'red':'green',
                        lineWidth: 2,
                        lineStyle: isPreSubmitted?LineStyle.Dashed:LineStyle.Dotted,
                        axisLabelVisible: true,
                    }
                    break
                }
            case 'TRAIL LIMIT':
                {
                    let isPreSubmitted = orderStatus.status == 'PreSubmitted'
                    line_option = {
                        price: isPreSubmitted?order.trailStopPrice:order.lmtPrice,
                        color: order.action == 'BUY'?'red':'green',
                        lineWidth: 2,
                        lineStyle: isPreSubmitted?LineStyle.Dashed:LineStyle.Dotted,
                        axisLabelVisible: true,
                    }
                    break
                }
                }

            if (this.orderLines[key]) {
                let line = this.orderLines[key]
                line.applyOptions(line_option)
            }else if (line_option) {
                let line = this.ohlcSeries.createPriceLine(line_option)
                this.orderLines[key] = line
            }
        },
        handleBars(bars) {
            this.bars = bars
            let barsArr = []
            let volArr = []
            let maArr = {5: [], 10: [], 30: [], 60: []}
            bars.forEach((element, index, arr) => {
                let t = new Date(element.time).getTime() / 1000 + 28800
                let bar = Object.assign({}, element, {'time': t})
                barsArr.push(bar)
                volArr.push({'time': t, 'value': bar.volume})
                for(let key in maArr) {
                    if(index < key){
                        maArr[key].push({'time': t, 'value': NaN})
                    }else{
                        let total = 0
                        arr.slice(index - key, index).forEach(b => total += b.close)
                        maArr[key].push({'time': t, 'value':total / key})
                    }
                }
            })
            this.ohlcSeries.setData(barsArr)
            this.volSeries.setData(volArr)
            for(let key in this.maSeries) {
                this.maSeries[key].setData(maArr[key])
            }
            // this.maSeries.setData(maArr)
            // this.trades.forEach(t => this.handleTrade(t))
        },
        handleBar(bar) {
            if (bar.time == this.bars[this.bars.length - 1].time) {
                Object.assign(this.bars[this.bars.length - 1], bar)
            }else{
                this.bars.push(bar)
            }

            const t = new Date(bar.time).getTime() / 1000 + 28800
            this.ohlcSeries.update(Object.assign({}, bar, {time: t}))
            this.volSeries.update({'time': t, 'value': bar.volume})
            for(let key in this.maSeries) {
                let sum = 0
                let size = this.ohlcSeries.series().data().size()
                for(let i = key;i > 0; i--){
                    sum += this.ohlcSeries.series().dataAt(size - i).close
                }
                this.maSeries[key].update({'time': t, 'value': sum / key})
            }
        },
        extendBarsBackWard(bars) {
            console.log('extendBarsBackWard')
            if (bars[bars.length - 1].time >= this.bars[0].time){
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Extend bars backward Failed!',
                    content: `backward last time:${bars[bars.length - 1].time} -> origin last time${this.bars[0].time}`,
                    timeout: 30000
                    })
                return
            }

            this.handleBars(bars.concat(this.bars))
        },
        onChartClick(param) {
            if (this.menu.isShow) {
                return
            }
            const price = this.ohlcSeries.coordinateToPrice(param.point.y)
            const lastPrice = this.ohlcSeries.series().bars().last().value[3]
            switch(true) {
                case this.contract && price > lastPrice && this.action == 'BUY':
                    {   
                        if(this.isTrail) {
                            this.sendOrder('TRAIL LIMIT', price, 'BUY', lastPrice)
                        }else{
                            this.sendOrder('STP LMT', price, 'BUY')
                        }
                        break
                    }    
                case this.contract && price < lastPrice && this.action == 'BUY':
                    {
                        if(this.isTrail) {
                            this.$bus.$emit('notice', {
                                color: 'error',
                                title: 'Order Failed!',
                                content: "不能开即刻触发的移动止损单",
                                timeout: 3000
                                })
                        }else {
                            this.sendOrder('LMT', price, 'BUY')
                        }
                        break
                    }
                case this.contract && price < lastPrice && this.action == 'SELL':
                    {
                        if(this.isTrail) {
                            this.sendOrder('TRAIL LIMIT', price, 'SELL', lastPrice)
                        }else {
                            this.sendOrder('STP LMT', price, 'SELL')
                        }
                        break
                    }
                    
                case this.contract && price > lastPrice && this.action == 'SELL':
                    {
                        if(this.isTrail) {
                            this.$bus.$emit('notice', {
                                color: 'error',
                                title: 'Order Failed!',
                                content: "不能开即刻触发的移动止损单",
                                timeout: 3000
                                })
                        }else {
                            this.sendOrder('LMT', price, 'SELL')
                        }
                        break
                    }
                default:
                    {
                        this.$bus.$emit('notice', {
                            color: 'error',
                            title: 'Order Failed!',
                            content: "请先选择合约和开单方向",
                            timeout: 3000
                        })
                    }
               
            }

            this.action = ""
        },
        onCrosshairMove({time, point, seriesPrices}) {
            if (
                !time ||
                !point ||
                point.x < 0 ||
                point.x > this.$refs.barChart.clientWidth ||
                point.y < 0 ||
                point.y > this.$refs.barChart.clientHeight
            ) {
                this.legend_bar = {time: NaN, open: NaN, high: NaN, low: NaN, close: NaN, volume: NaN}
                this.legend_ma = {5: NaN, 10: NaN, 30: NaN, 60: NaN}
            }else{
                this.legend_bar.time = time
                Object.assign(this.legend_bar, seriesPrices.get(this.ohlcSeries))
                this.legend_bar.volume = seriesPrices.get(this.volSeries)
                for(let key in this.legend_ma) {
                    this.legend_ma[key] = seriesPrices.get(this.maSeries[key])
                }
            }
        },
        onTimeRangeChange(param) {
            if (this.ohlcSeries.series().bars().first().time.timestamp == param.from){
                this.$ibws.once('bars_', this.extendBarsBackWard)
                this.$ibws.send({action: 'get_klines', 'contract': this.contract, 'duration': '1 D', 'end': new Date((param.from - 28800) * 1000), 'barSize': this.barSize})
            }
        },
        gotoForefront() {
            const visibleRange = this.chart.timeScale().getVisibleRange()
            const range = visibleRange.to - visibleRange.from
            const forefrontTS = this.ohlcSeries.series().bars().last().time.timestamp

            this.chart.timeScale().setVisibleRange({from: forefrontTS - range, to: forefrontTS})
            
        },
        sendOrder(orderType, price, action, lastPrice) {
            // if no action , notice error
            if(!(this.contract && action)) return

            // let order = new Order()
            // order.outsideRth = true
            // order.orderType = orderType
            // order.action = action
            // order.tif = 'GTC'
            // order.totalQuantity = parseInt(this.volume)

            let order = null

            switch(orderType) {
                case 'LMT':
                    {
                        // order.lmtPrice = parseInt(price)
                        // order.orderRef = `ct-${order.totalQuantity}@${order.lmtPrice}`
                        order = Order.NewLimitOrder(action, price, this.volume, '#ct')
                        break
                    }
                    
                case 'STP LMT':
                    {
                        // let offset = parseInt(action == 'BUY'?this.offset:-this.offset)
                        // order.lmtPrice = parseInt(price)
                        // order.auxPrice = order.lmtPrice + offset
                        // order.orderRef = `ct-sl-${order.totalQuantity}@${order.auxPrice}->${order.lmtPrice}`
                        let offset = action == 'BUY'?this.offset:-this.offset
                        order = Order.NewStopLimitOrder(action, price, price + offset, this.volume, '#ct')
                        break
                    }
                case 'TRAIL LIMIT':
                    {
                        // order.trailStopPrice = parseInt(price)
                        // order.auxPrice = Math.round(Math.abs(lastPrice - price))
                        // order.triggerMethod = 4
                        // order.lmtPriceOffset = parseInt(this.offset)
                        // order.orderRef = `ct-trailsl-${order.totalQuantity}@^${order.trailStopPrice}->${order.auxPrice}[${order.lmtPriceOffset}]`
                        order = Order.NewTrailStopOrder(action, price, this.offset, Math.abs(lastPrice-price), this.volume, '#ct')
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
        },
        onResize() {
            if (this.chart) {
                this.chart.applyOptions({
                    width: this.$refs.barChart.clientWidth, 
                    height: this.$refs.barChart.clientHeight,
                    })
            }
        },
        get_datas() {
            let bs = this.ohlcSeries.series().bars()
            let close = bs.vi.slice(bs.lastIndex()-120, bs.lastIndex()).map((v)=>v.value[3])
            return close
        }
        
        // predict() {
        //     this.showPredict = true
        //     // let bs = this.ohlcSeries.series().bars()
        //     // let close = bs.vi.slice(bs.lastIndex()-120, bs.lastIndex()).map((v)=>v.value[3])

        //     // let temp_form = document.createElement("form")
        //     // temp_form.action = '../api/predict'
        //     // temp_form.target = '_blank'
        //     // temp_form.method = 'post'
        //     // temp_form.style.display = 'none'

        //     // let opt_data = document.createElement('textarea')
        //     // opt_data.name = "data"
        //     // opt_data.value = close

        //     // let opt_from = document.createElement('textarea')
        //     // opt_from.name = "from"
        //     // opt_from.value = '20180101'

        //     // document.body.appendChild(temp_form)
        //     // temp_form.appendChild(opt_data)
        //     // temp_form.appendChild(opt_from)
        //     // temp_form.submit()
        //     // document.body.removeChild(temp_form)


        //     // this.$axios.post('../api/predict', {"data": close, "from": '20180101'}).then(
        //     //     (res)=>{
        //     //         console.log(res)
        //     //         window.open()
        //     //     })
        // },
    },
    beforeDestroy() {
        if (this.contract) {
            this.$ibws.send({'action': 'unsub_klines', 'contract': this.contract, 'barSize': this.barSize})
        }  
        this.$ibws.off('bars')
        this.$ibws.off('bar')
	},


}
</script>
<style lang="scss">
    #bar-chart {
    position: relative;
    &:hover .legend {
        opacity: 1;
    }
    }

    .action {
    position: absolute;
    top: 1em;
    right: 5em;
    z-index: 3;
    opacity: .2;
    &:hover {
        opacity: 1;
    }
    transition: opacity .2s cubic-bezier(0.005, 1, 0.22, 1);
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    }

    .action-active {
    opacity: 1;
    color: 'blue';
    }

    #forefront {
    bottom: 4em;
    left: 1em;
    z-index: 3;
    opacity: .5;
    transition: opacity .2s cubic-bezier(0.005, 1, 0.22, 1);
    display: flex;
    flex-direction: column;
    &:hover {
        opacity: 1;
    }
    }
</style>