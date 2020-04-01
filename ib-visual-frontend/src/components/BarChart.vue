<template>
    <v-chart :options="kline"></v-chart>
</template>
<script>
// import ContractItem from '../ContractItem.vue'
let upColor = '#00da3c'
let downColor = '#ec0000'
export default {
    props: ['contract'],
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
                        start: 98,
                        end: 100
                    },
                    {
                        show: true,
                        xAxisIndex: [0, 1],
                        type: 'slider',
                        top: '85%',
                        start: 98,
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
                            tooltip: [0, 1, 2, 3]
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
                    // {
                    //     name: 'MA5',
                    //     type: 'line',
                    //     data: calculateMA(5, data),
                    //     smooth: true,
                    //     lineStyle: {
                    //         opacity: 0.5
                    //     }
                    // },
                    // {
                    //     name: 'MA10',
                    //     type: 'line',
                    //     data: calculateMA(10, data),
                    //     smooth: true,
                    //     lineStyle: {
                    //         opacity: 0.5
                    //     }
                    // },
                    // {
                    //     name: 'MA20',
                    //     type: 'line',
                    //     data: calculateMA(20, data),
                    //     smooth: true,
                    //     lineStyle: {
                    //         opacity: 0.5
                    //     }
                    // },
                    // {
                    //     name: 'MA30',
                    //     type: 'line',
                    //     data: calculateMA(30, data),
                    //     smooth: true,
                    //     lineStyle: {
                    //         opacity: 0.5
                    //     }
                    // },
                    {
                        name: 'Volume',
                        type: 'bar',
                        xAxisIndex: 1,
                        yAxisIndex: 1,
                        encode: {
                            x: 'date',
                            y: 'volume',
                        }
                    }
                ]

            }
        }
    },

    mounted() {
        var _this = this
        this.$ibws.on('bars', function(bars){
            console.log(bars.data)
            _this.kline.dataset.source = bars.data
        })

        this.$ibws.on('bar', function(bar){
            console.log(bar)
            let i = _this.kline.dataset.source.length - 1
            console.log(_this.kline.dataset.source[i])
            if (_this.kline.dataset.source[i] && bar.data.date == _this.kline.dataset.source[i].date){
                _this.kline.dataset.source.splice(i, 1, bar.data)
            }else{
                _this.kline.dataset.source.push(bar.data)
            }

        })

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
    
    }

    // methods: {

    // }
}
</script>
<style scoped>
    .echarts {
        width: 1200px;
        height: 600px;
        }
</style>