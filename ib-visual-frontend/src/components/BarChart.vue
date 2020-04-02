<template>
    <v-chart :options="kline" @datazoom=dz @click=insertOrder></v-chart>
</template>
<script>
// import ContractItem from '../ContractItem.vue'
import Vue from 'vue'
let upColor = '#00da3c'
let downColor = '#ec0000'
function calculateMA(dayCount, data) {
    var result = [];
    for (var i = 0, len = data.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-')
            continue
        }
        var sum = 0
        for (var j = 0; j < dayCount; j++) {
            sum += data[i - j]
        }
        result.push(sum / dayCount)
    }
    return result
}


export default {
    components:{
        // ContractItem
    },

    data() {
        return {
            // contractList: [],
            kline: {
                dataset: {
                    dimensions: ['date', 'open', 'close', 'low', 'high', 'volume'],
                    source: [],
                },
                legend: {
                    top: 30,
                    data: ['KLine', 'Volume', 'MA5', 'MA10', 'MA20', 'MA30']
                    },
                title: {
                    text: "行情",
                    left: 0,
                },
                tooltip: {
                    trigger: "axis",
                    axisPointer: {
                        type: "cross"
                    },
                    backgroundColor: 'rgba(245, 245, 245, 0.8)',
                    borderWidth: 1,
                    borderColor: '#ccc',
                    padding: 10,
                    textStyle: {
                        color: '#000'
                    },
                    position: function (pos, params, el, elRect, size) {
                        var obj = {top: 10};
                        obj[['left', 'right'][+(pos[0] < size.viewSize[0] / 2)]] = 30;
                        return obj;
                    }
                },
                axisPointer: {
                    link: {xAxisIndex: 'all'},
                    label: {
                        backgroundColor: '#777'
                    }
                },
                toolbox: {
                    feature: {
                        dataZoom: {
                            yAxisIndex: false
                        },
                        brush: {
                            type: ['lineX', 'clear']
                        }
                    }
                },
                brush: {
                    xAxisIndex: 'all',
                    brushLink: 'all',
                    outOfBrush: {
                        colorAlpha: 0.1
                    }
                },
                visualMap: {
                    show: false,
                    seriesIndex: 5,
                    dimension: 2,
                    pieces: [{
                        value: 1,
                        color: downColor
                    }, {
                        value: -1,
                        color: upColor
                    }]
                },
                grid: [
                    {
                        left: '10%',
                        right: '8%',
                        height: '50%'
                    },
                    {
                        left: '10%',
                        right: '8%',
                        top: '63%',
                        height: '16%'
                    }
                ],
                xAxis: [
                    {
                        type: 'category',
                        gridIndex: 0,
                        scale: true,
                        boundaryGap: false,
                        axisLine: {onZero: false},
                        splitLine: {show: false},
                        splitNumber: 20,
                        min: 'dataMin',
                        max: 'dataMax',
                        axisPointer: {
                            z: 100
                        }
                    },
                    {
                        type: 'category',
                        gridIndex: 1,
                        scale: true,
                        boundaryGap: false,
                        axisLine: {onZero: false},
                        axisTick: {show: false},
                        splitLine: {show: false},
                        axisLabel: {show: false},
                        splitNumber: 20,
                        min: 'dataMin',
                        max: 'dataMax'
                    }
                ],
                yAxis: [
                    {
                        scale: true,
                        gridIndex: 0,
                        splitArea: {
                            show: true
                        }
                    },
                    {
                        scale: true,
                        gridIndex: 1,
                        splitNumber: 2,
                        axisLabel: {show: false},
                        axisLine: {show: false},
                        axisTick: {show: false},
                        splitLine: {show: false}
                    }
                ],
                dataZoom: [
                    {
                        type: 'inside',
                        xAxisIndex: [0, 1],
                        start: 60,
                        end: 100
                    },
                    {
                        show: true,
                        xAxisIndex: [0, 1],
                        type: 'slider',
                        top: '85%',
                        start: 60,
                        end: 100
                    }
                ],
                series: [
                    {
                        name: "KLine",
                        type: 'candlestick',
                        itemStyle: {
                            color: upColor,
                            color0: downColor,
                            borderColor: null,
                            borderColor0: null
                        },
                        encode:{
                            tooltip: [1, 2, 3, 4]
                        },
                        // tooltip: {
                        //     formatter: function (param) {
    
                                // param = param[0]
                                // return [
                                //     'Date: ' + param.name + '<hr size=1 style="margin: 3px 0">',
                                //     'Open: ' + param.data.open + '<br/>',
                                //     'Close: ' + param.data.close + '<br/>',
                                //     'Low: ' + param.data.low + '<br/>',
                                //     'High: ' + param.data.high + '<br/>'
                                // ].join('');
                            // }
                        // }
                    },
                    {
                        name: 'Volume',
                        type: 'bar',
                        xAxisIndex: 1,
                        yAxisIndex: 1,
                        encode: {
                            x: 'date',
                            y: 'volume',
                        }
                    },
                    {
                        name: 'MA5',
                        type: 'line',
                        data: [],
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                    {
                        name: 'MA10',
                        type: 'line',
                        data: [],
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                    {
                        name: 'MA20',
                        type: 'line',
                        data: [],
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                    {
                        name: 'MA30',
                        type: 'line',
                        data: [],
                        smooth: true,
                        lineStyle: {
                            opacity: 0.5
                        }
                    },
                ]

            }
        }
    },
    computed:{
        contract() {
            return this.$store.state.currentContract
        }
    },
    created: () => {
		// 在实例创建完成后被立即调用。在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。然而，挂载阶段还没开始，$el 属性目前不可见。
        console.log('created')
    },
    beforeMount: () => {
        // 在挂载开始之前被调用：相关的 render 函数首次被调用。
        console.log('beforeMount')
	},

    mounted() {
        console.log('mounted')






        var _this = this
        this.$ibws.on('bars', function(bars){
            // console.log(bars)
            _this.kline.dataset.source = bars
            let c = []
            for (var d of _this.kline.dataset.source){
                c.push(d.close)
            }
            console.log(c)
            _this.kline.series[2].data = calculateMA(5, c)
            _this.kline.series[3].data = calculateMA(10, c)
            _this.kline.series[4].data = calculateMA(20, c)
            _this.kline.series[5].data = calculateMA(30, c)
            console.log(_this.kline.series[1].data)
        })

        this.$ibws.on('bar', function(bar){
            // console.log(bar)
            let i = _this.kline.dataset.source.length - 1
            // console.log(_this.kline.dataset.source[i])
            if (_this.kline.dataset.source[i] && bar.date == _this.kline.dataset.source[i].date){
                _this.kline.dataset.source.splice(i, 1, bar)
            }else{
                _this.kline.dataset.source.push(bar)
                let c = []
                for (var d of _this.kline.dataset.source){
                    c.push(d.close)
                }
                _this.kline.series[2].data = calculateMA(5, c)
                _this.kline.series[3].data = calculateMA(10, c)
                _this.kline.series[4].data = calculateMA(20, c)
                _this.kline.series[5].data = calculateMA(30, c)
            }
        })


        if (this.contract){
            this.$ibws.send({'action': 'sub_klines', 'contract': this.contract})
        }
        

        // this.$ibws.on('contract', function(c) {
        //     var flag = true
        //     _this.contractsList.forEach(element => {
        //         if (element.conId === c.conId){
        //             flag = false
        //         }
        //     })
        //     if (flag){
        //         _this.contractsList.push(c)
        //     }
        // })
    
    },
    beforeUpdate: () => {
        // 数据更新时调用，发生在虚拟 DOM 打补丁之前。这里适合在更新之前访问现有的 DOM，比如手动移除已添加的事件监听器。
        console.log('beforeUpdate')
	},
	updated: () => {
		// 由于数据更改导致的虚拟 DOM 重新渲染和打补丁，在这之后会调用该钩子。
		// 当这个钩子被调用时，组件 DOM 已经更新，所以你现在可以执行依赖于 DOM 的操作。然而在大多数情况下，你应该避免在此期间更改状态。如果要相应状态改变，通常最好使用计算属性或 watcher 取而代之。
        // 注意 updated 不会承诺所有的子组件也都一起被重绘。
        console.log('updated')
	},
	activated: () => {
        // keep-alive 组件激活时调用。
        console.log('activated')
	},
	deactivated: () => {
        // keep-alive 组件停用时调用。
        console.log('deactivated')
	},
	beforeDestroy: () => {
        // 实例销毁之前调用。在这一步，实例仍然完全可用。
        console.log('beforeDestroy')
        Vue.$ibws.send({'action': 'unsub_klines'})
        Vue.$ibws.off('bars')
        Vue.$ibws.off('bar')
	},
	destroyed: () => {
        // Vue 实例销毁后调用。调用后，Vue 实例指示的所有东西都会解绑定，所有的事件监听器会被移除，所有的子实例也会被销毁。
        console.log('destroyed')
	},

    methods: {
        dz(event) {
            if (event.batch){
                this.kline.dataZoom[0].start = event.batch[0].start
                this.kline.dataZoom[0].end = event.batch[0].end
                // this.kline.dataZoom[1].start = event.batch[0].start
                // this.kline.dataZoom[1].end = event.batch[0].end
            }else{
                this.kline.dataZoom[0].start = event.start
                this.kline.dataZoom[0].end = event.end
                // this.kline.dataZoom[1].start = event.start
                // this.kline.dataZoom[1].end = event.end
            }
            
        },
        insertOrder(x, y){
            console.log(x)
            console.log(y)
        }
    }
}
</script>
<style scoped>
    .echarts {
        width: 1500px;
        height: 600px;
        }
</style>