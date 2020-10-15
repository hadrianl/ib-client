<template>
    <v-dialog 
    v-model="showPredict"
    eager
    fullscreen
    hide-overlay
    transition="dialog-bottom-transition">
        <template v-slot:activator="{ attrs }">
            <v-btn
            color="red lighten-2"
            dark
            :disabled="btn_disabled"
            v-bind="attrs"
            @click="predict"
            >
            {{$t('button.predict')}}
            </v-btn>
        </template>
        <v-card>
            <v-toolbar
            dark
            color="primary"
            >
            <v-btn
                icon
                dark
                @click="showPredict = false"
            >
                <v-icon>mdi-close</v-icon>
            </v-btn>
            <v-toolbar-title>{{$t('button.predict')}}</v-toolbar-title>
            <v-spacer></v-spacer>
            <!-- <v-toolbar-items>
                <v-btn
                dark
                text
                @click="exportChart"
                >
                Export
                </v-btn>
            </v-toolbar-items> -->
            </v-toolbar>
            <!-- <HighCharts ref="highchart" id="container"></HighCharts> -->
            <highcharts ref="hc" :options="options"></highcharts>
        </v-card>
    </v-dialog>
</template>
<script>
// import HighCharts from './charts/HighChart.vue'

export default {
    components: {
        // HighCharts,
    },
    data() {
        return {
            btn_disabled: false,
            options: {
                chart: {
                    type: 'line'
                },
                title: {
				text: 'HSI预测'
                },
                legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle'
                },
                xAxis: [
                    {type: 'datetime'},
                    {type: 'linear', visible: false}
                ],
                series: [],
                responsive: {
                        rules: [{
                                condition: {
                                        maxWidth: 500
                                },
                                chartOptions: {
                                        legend: {
                                                layout: 'horizontal',
                                                align: 'center',
                                                verticalAlign: 'bottom'
                                        }
                                }
                        }]
                },
                plotOptions: {
                    arearange: {
                        marker: {
                            enabled: false,
                        }
                    },
                    line: {
                        marker: {
                            enabled: false,
                        }
                    },
                }
            },
            showPredict: false,
            }
    },
    props: [
        'get_datas',
    ],
    mounted() {
    },
    methods: {
        predict() {
            console.log(this)
            let { close } =  this.get_datas()
            this.btn_disabled = true
            this.$axios.post('../api/predict', {"data": close, "from": '20180101'}).then(
                (res)=>{
                    let series = [
                        {
                            name: "latest",
                            data: res.data.ts_target_mv,
                            color: "red",
                            lineWidth: 3,
                            zIndex: 3,
                            xAxis: 1,
                        }
                    ]

                    let target_count = res.data.ts_target_mv.length
                    res.data.ts_src_mvs.forEach((arr, index)=>{
                        series.push(
                            {
                                name: "his top " + (index + 1).toString(),
                                data: arr,
                                dashStyle: "ShortDashDot",
                                visible: index < 3,
                                lineWidth: 1,
                                zIndex: 0,
                                xAxis: 1,
                            },
                        )
                    })

                    series.push(
                        {
                            name: "predict_mean",
                            data: Array(target_count).fill('-').concat(res.data.pmean),
                            color: "red",
                            dashStyle: "ShortDot",
                            lineWidth: 3,
                            zIndex: 3,
                            xAxis: 1,
                        }
                    )

                    for (let n in res.data.pstd){
                        let std = res.data.pstd[n]
                        let data = []
                        res.data.pmean.forEach((v, i)=>{
                            data.push([v + std[i], v - std[i]])
                        })
                        series.push(
                        {
                            name: 'predict_std_' + n,
                            type: 'arearange',
                            data: Array(target_count).fill('-').concat(data),
                            zIndex: 2,
                            xAxis: 1,
                        }
                    )
                    }
                    
                    this.options.series = series
                    console.log(series)
                    this.showPredict = true
                }).then(()=>{this.btn_disabled = false}).catch(err => {
                    console.log(err)
                    this.btn_disabled = false
                })
        },
        exportChart() {
            console.log(this.$refs.hc)
            this.$refs.hc.chart.exportChartLocal({type: 'image/svg+xml', filename: 'hsi_predict', scale: 4})
        }
    },

}
</script>