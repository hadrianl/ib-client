<template>
    <v-container fluid class='mt-1 pt-1'>
        <v-card ref="barCard" :color="colors.background">
            <v-toolbar dense flat :color="colors.background">
                <v-btn-toggle v-model="barSize" rounded mandatory dense borderless dark class='period'>
                <v-btn value="1 min">1 min</v-btn>
                <v-btn value="3 mins">3 mins</v-btn>
                <v-btn value="5 mins">5 mins</v-btn>
                <v-btn value="10 mins">10 mins</v-btn>
                <v-btn value="15 mins">15 mins</v-btn>
                </v-btn-toggle>
                <v-spacer></v-spacer>
                <v-switch v-model="isTrail" label="Trail" dark dense hide-details></v-switch>
                <v-btn-toggle v-model="action" rounded dense>
                    <v-btn value="BUY" color="red">BUY</v-btn>
                    <v-btn value="SELL" color="green">SELL</v-btn>
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
                    <div ref="barChart" class="ChartContainer" id="bar-chart" @contextmenu.prevent="showMenu">
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
                                    <v-list-item-title>Cancel All</v-list-item-title>
                                </v-list-item>
                            </v-list>
                        </v-menu>
                        <Legend :legend_bar="legend_bar" :legend_ma="legend_ma"></Legend>
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

export default {
    components: {
        Legend,
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
            console.log(arr)
            arr.sort((a, b)=>a.time - b.time)
            return arr
        }
    },
    data() {
        return {
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
            }
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
            }
        }
        this.chart = createChart(this.$refs.barChart, chartOptions)
        this.ohlcSeries = this.chart.addCandlestickSeries()
        this.volSeries = this.chart.addHistogramSeries({base: 0, overlay: true})
        // this.maSeries = this.chart.addLineSeries()
        let colors = {5: '#DC143C', 10: '#FFC125', 30: '#C0FF3E', 60: '#97FFFF'}
        for(let key in this.maSeries){
            this.maSeries[key] = this.chart.addLineSeries({
                priceLineVisible: false, 
                lastValueVisible: false, 
                lineWidth: 1, 
                color: colors[key],
                })
        }
        this.chart.applyOptions({
            crosshair: {
                mode: 0
            }
        })
        this.ohlcSeries.applyOptions({
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
        })
        this.volSeries.applyOptions({
            color: '#6495ED',
            scaleMargins: {
                top: 0.6,
                bottom: 0.02
            }
        })

        // var _this = this
        this.chart.subscribeClick(this.onChartClick)
        this.chart.subscribeCrosshairMove(this.onCrosshairMove)
        // this.chart.subscribeVisibleTimeRangeChange(this.onTimeRangeChange)

        this.$ibws.on('trade', this.handleTrade)

        this.$ibws.on('bars', this.handleBars)

        this.$ibws.on('bar', this.handleBar)

        this.$ibws.once('bars', this.initAddition)

        if (this.contract){
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract})
        }

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
                
            case 'STP LMT': case 'LIT':
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
            case 'TRAIL LIMIT':
                {
                    let isPreSubmitted = t.orderStatus.status == 'PreSubmitted'
                    line_option = {
                        price: isPreSubmitted?t.order.trailStopPrice:t.order.lmtPrice,
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
                let line = this.ohlcSeries.createPriceLine(line_option)
                this.orderLines[key] = line
                }
        },
        handleBars(bars) {
            let volArr = []
            let maArr = {5: [], 10: [], 30: [], 60: []}
            bars.forEach((element, index, arr) => {
                let t = new Date(element.time).getTime() / 1000 + 28800
                bars[index].time = t
                volArr.push({'time': t, 'value': element.volume})
                for(let key in maArr) {
                    if(index < key){
                        maArr[key].push({'time': t, 'value': NaN})
                    }else{
                        let sum = 0
                        arr.slice(index - key, index).forEach(b => sum += b.close)
                        maArr[key].push({'time': t, 'value':sum / key})
                    }
                }
            })
            this.ohlcSeries.setData(bars)
            this.volSeries.setData(volArr)
            for(let key in this.maSeries) {
                this.maSeries[key].setData(maArr[key])
            }
            // this.maSeries.setData(maArr)
            // this.trades.forEach(t => this.handleTrade(t))
        },
        handleBar(bar) {
            const t = new Date(bar.time).getTime() / 1000 + 28800
            bar.time = t
            this.ohlcSeries.update(bar)
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
        onCrosshairMove(param) {
            if (
                param === undefined ||
                param.time === undefined ||
                param.point.x < 0 ||
                param.point.x > this.$refs.barChart.clientWidth ||
                param.point.y < 0 ||
                param.point.y > this.$refs.barChart.clientHeight
            ) {
                this.legend_bar = {time: NaN, open: NaN, high: NaN, low: NaN, close: NaN, volume: NaN}
                this.legend_ma = {5: NaN, 10: NaN, 30: NaN, 60: NaN}
            }else{
                this.legend_bar.time = param.time
                Object.assign(this.legend_bar, param.seriesPrices.get(this.ohlcSeries))
                this.legend_bar.volume = param.seriesPrices.get(this.volSeries)
                for(let key in this.legend_ma) {
                    this.legend_ma[key] = param.seriesPrices.get(this.maSeries[key])
                }
            }
        },
        onTimeRangeChange(param) {
            setTimeout(function(){
                console.log(param.from)
                console.log(param.to)
            }, 10000)
        },
        sendOrder(orderType, price, action, lastPrice) {
            // if no action , notice error
            if(!(this.contract && action)) {
                return
            }

            let order = new Order()
            order.outsideRth = true
            order.orderType = orderType
            order.action = action
            order.tif = 'GTC'
            order.totalQuantity = parseInt(this.volume)

            switch(orderType) {
                case 'LMT':
                    {
                        order.lmtPrice = parseInt(price)
                        order.orderRef = `ct@${order.lmtPrice}`
                        break
                    }
                    
                case 'STP LMT':
                    {
                        let offset = parseInt(action == 'BUY'?this.offset:-this.offset)
                        order.lmtPrice = parseInt(price)
                        order.auxPrice = order.lmtPrice + offset
                        order.orderRef = `ct@${order.auxPrice}->${order.lmtPrice}`
                        break
                    }
                case 'TRAIL LIMIT':
                    {
                        order.trailStopPrice = parseInt(price)
                        order.auxPrice = Math.round(Math.abs(lastPrice - price))
                        order.triggerMethod = 4
                        order.lmtPriceOffset = parseInt(this.offset)
                        order.orderRef = `ct@^${order.trailStopPrice}->${order.auxPrice}[${order.lmtPrice}]`
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
</style>