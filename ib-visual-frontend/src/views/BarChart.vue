<template>
    <v-container fluid class='mt-1 pt-1'>
        <v-card ref="barCard">
            <v-responsive :aspect-ratio="16/9">
                <v-card-text>
                    <div ref="barChart" class="ChartContainer" id="bar-chart"></div>
                </v-card-text>
                <v-card-actions>
                    <v-row>
                        <v-col>
                            <v-btn-toggle v-model="barSize" rounded mandatory>
                            <v-btn value="1 min">1 min</v-btn>
                            <v-btn value="5 mins">5 mins</v-btn>
                            <v-btn value="10 mins">10 mins</v-btn>
                            <v-btn value="15 mins">15 mins</v-btn>
                            </v-btn-toggle>
                        </v-col>
                        <v-col>
                            <v-btn-toggle v-model="action" rounded>
                            <v-btn value="BUY" color="red">BUY</v-btn>
                            <v-btn value="SELL" color="green">SELL</v-btn>
                            </v-btn-toggle>
                        </v-col>
                        <v-col>
                            <v-row>
                                <v-text-field 
                                v-model="volume" 
                                label="volume" 
                                type="number" 
                                outlined>
                                </v-text-field>
                                <v-text-field 
                                v-model="offset" 
                                label="offset" 
                                type="number" 
                                outlined 
                                hide-details>
                                    <template v-slot:prepend>
                                        <v-icon
                                        :color="action?action=='BUY'?'red':'green':''"
                                        >{{action?action=='BUY'?'mdi-arrow-collapse-up':'mdi-arrow-collapse-down':''}}</v-icon>
                                    </template>
                                </v-text-field>
                            </v-row> 
                        </v-col>
                        <v-spacer />
                    </v-row>
                </v-card-actions>
            </v-responsive>
        </v-card>
    </v-container>
    

</template>
<script>
import { createChart, LineStyle} from 'lightweight-charts'
import {Order} from '../plugins/datastructure.js'
import {orderKey} from '../store/store.js'

export default {
    props: {
        // chartWidth: {
        //     type: Number,
        //     default: 1300
        // },
        // chartHeight: {
        //     type: Number,
        //     default: 500
        // }
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
            chartWidth: 1600,
            chartHeight: 500,
            ohlcSeries: null,
            volSeries: null,
            maSeries: null,
            orderLines: {},
            tradeMarkers: {},
            barSize: "1 min",
            action: "",
            volume: 1,
            offset: 0,
        }
    },
    mounted() {
        console.log(this.chartWidth)
        const chartOptions = {
            width: this.chartWidth, 
            height: this.chartHeight,
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

        // this.$on('changeContract', function(payload) {
        //     console.log('recv_changeContract')
        //     let oldCon = payload.old
        //     let newCon = payload.new
        //     console.log(`newCon:${newCon}`)
        //     console.log(`oldCon:${oldCon}`)
        //     if (oldCon) {
        //         this.$ibws.send({'action': 'unsub_klines', 'contract': oldCon})
        //     }

        //     this.$ibws.once('bars', this.initAddition)
        //     this.$ibws.send({'action': 'sub_klines', 'contract': this.contract})
        // }
        // )
    },
    watch: {
        contract(newCon, oldCon) {
            console.log(`newCon:${newCon}`)
            console.log(`oldCon:${oldCon}`)
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
        chartWidth(w) {
            if (this.chart) {
                this.chart.applyOptions({
                    width: w, 
                    height: this.chartHeight,
                    })
            }
        },
        chartHeight(h) {
            if (this.chart) {
                this.chart.applyOptions({
                    width: this.chartWidth, 
                    height: h,
                    })
            }
        }
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
                        let offset = parseInt(action == 'BUY'?this.offset:-this.offset)
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
    beforeDestroy() {
        if (this.contract) {
            this.$ibws.send({'action': 'unsub_klines', 'contract': this.contract, 'barSize': this.barSize})
        }  
        this.$ibws.off('bars')
        this.$ibws.off('bar')
	},


}
</script>