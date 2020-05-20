import * as lwc from 'lightweight-charts'
import seriesData from './series.js'
import indicators from './indicator.js'

const type2SeriesFunc = {
    Candlestick: 'addCandlestickSeries',
    Histogram: 'addHistogramSeries',
    Line: 'addLineSeries',

}

export default class ChartController {
    constructor() {
        this.chart = null
        this.el = null
        this.Series = {}
        this.indicators = {}

    }

    createChart(el, options) {
        this.el = el
        this.chart = lwc.createChart(el, options)
        this.setBaseSeries()
        this.setIndicatorSeries()
    }

    setBaseSeries() {
        for (let [k , v] of Object.entries(seriesData)){
            this.Series[k] = this.chart[type2SeriesFunc[v.type]]()
            this.Series[k].applyOptions(v.options)
        }
        
    }

    setIndicatorSeries() {
        for (let [i, inds] of Object.entries(indicators)) {
            this.indicators[i] = {}
            for (let [k, v] of Object.entries(inds)) {
                this.indicators[i][k] = this.chart[type2SeriesFunc[v.type]]()
                this.indicators[i][k].applyOptions(v.options)
            }
        }
    }

    handleBars(bars) {
        this.bars = bars
        let barsArr = []
        let volArr = []
        let maArr = {}
        this.indicators['ma'].keys().forEach((k) => maArr[k] = [])
    
        bars.forEach((element, index, arr) => {
            let t = new Date(element.time).getTime() / 1000 + 28800
            let bar = Object.assign({}, element, {'time': t})
            barsArr.push(bar)
            volArr.push({'time': t, 'value': bar.volume})
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
        this.Series['ohlc'].setData(barsArr)
        this.Series['vol'].setData(volArr)
        for(let key in this.indicators['ma']) {
            this.indicators['ma'][key].setData(maArr[key])
        }
        // this.maSeries.setData(maArr)
        // this.trades.forEach(t => this.handleTrade(t))
    }

    handleBar(bar) {
        if (bar.time == this.bars[this.bars.length - 1].time) {
            Object.assign(this.bars[this.bars.length - 1], bar)
        }else{
            this.bars.push(bar)
        }

        const t = new Date(bar.time).getTime() / 1000 + 28800
        this.Series['ohlc'].update(Object.assign({}, bar, {time: t}))
        this.Series['vol'].update({'time': t, 'value': bar.volume})
        for(let key in this.indicators['ma']) {
            let sum = 0
            let size = this.Series['ohlc'].series().data().size()
            for(let i = key;i > 0; i--){
                sum += this.Series['ohlc'].series().dataAt(size - i).close
            }
            this.indicators['ma'][key].update({'time': t, 'value': sum / key})
        }
    }
}