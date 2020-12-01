<template>
    <v-card align-stretch>
    <v-tabs vertical>
      <v-tab>
        {{$t('analysisTab.trend')}}
      </v-tab>
      <v-tab>
        {{$t('analysisTab.heatmap')}}
      </v-tab>
      <v-tab-item>
        <v-card flat>
            <highcharts ref='sc' :options="line_options"></highcharts>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
            <highcharts ref='tm' :options="treemap_options"></highcharts>
        </v-card>
      </v-tab-item>
    </v-tabs>
  </v-card>
</template>
<script>
// import {InfluxDB} from 'influx'

export default {
        data() {
            return {
                // window: 0,
                // influxclient: null,
                line_options: {
                    chart: {
                        height: window.innerHeight - 100,
                        spacingRight: 50,
                    },
                    title: {
                        text: 'HSI贡献度趋势',
                    },
                    credits: {
                        enabled: false,
                    },
                    rangeSelector: {
                        enabled: false
                    },
                    legend: {
                        enabled: true,
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle'
                    },
                    xAxis: [
                        {type: 'datetime'},
                    ],
                    navigation: {
                        buttonOptions: {
                            align: 'left',
                        },
                    },
                    tooltip: {
                        split: false,
                    },
                    series: [],
                },
                treemap_options: {
                    chart: {
                        height: window.innerHeight - 100,
                        spacingRight: 50,
                    },
                    title: {
                        text: 'HSI贡献度热力图',
                    },
                    credits: {
                        enabled: false,
                    },
                    navigation: {
                        buttonOptions: {
                            align: 'left',
                        },
                    },
                    series: [],
                    showCheckbox: true,
                },
                intervalTimer: null,
                capitals: {},
            }
        },
        async mounted() {
            // const host = 'localhost'
            // const port = 8087
            // const database = 'index_info'
            // this.influxclient = new InfluxDB({host, port, database})
            await this.getStockCapital()
            await this.updateLine()
            await this.updateHeatMap()
            this.intervalTimer = setInterval(async () => {
                await this.updateLine()
                await this.updateHeatMap()
            }, 60000)

            console.log(this)
        },
        methods: {
            async updateHeatMap() {
                // console.log('updateHeatMap')
                const query_last_sql = "select last(contribution), time from contribution where index_code='HSI' group by stock_code, stock_name"
                const ret = await this.axios.get('../influxdb/query', {params: {q: query_last_sql, db: 'index_info'}})

                let treemap = {
                        type: "treemap",
                        name: "HSI",
                        layoutAlgorithm: 'squarified',
                        alternateStartingDirection: true,
                        tooltip: {
                            pointFormat: '<b>{point.time}</b><br/><br>{point.name}</br>: {point.y}<br/>'
                        },
                        pointPadding: 3,
                        data: [],
                    }
                ret.data.results[0].series.forEach(({tags: {stock_name}, values: [[time, last]]}) => {
                    treemap.data.push({name: stock_name, value: Math.abs(last), color: last>=0?'red':'green', time: time, y: last })
                })
                console.log(treemap)
                this.treemap_options.series = [treemap]
                // console.log(this.treemap_options)

            },
            async updateLine() {
                const sql = "select contribution from contribution where index_code='HSI' and time > now() - 6h group by stock_code, stock_name"

                const ret = await this.axios.get('../influxdb/query', {params: {q: sql, db: 'index_info'}})

                let series = []
                

                ret.data.results[0].series.forEach(({tags: {stock_code, stock_name}, values}) => {
                    let line = {type: 'line', name: stock_name, data: [], visible: this.capitals[stock_code] < 10, id: stock_code, legendIndex: this.capitals[stock_code]}
                    values.forEach(([time, contribution]) => line.data.push([Date.parse(time) - 8*60*60*1000, contribution]))
                    series.push(line)
                })


                this.line_options.series = series
                // console.log(this.line_options)

            },
            async getStockCapital() {
                const sql = "select last(capital) from stock_info group by stock_code, stock_name"

                const ret = await this.axios.get('../influxdb/query', {params: {q: sql, db: 'index_info'}})

                // eslint-disable-next-line no-unused-vars
                let caps = ret.data.results[0].series.map(({tags: {stock_code}, values: [[time, cap]]}) => {return {stock_code, cap}}).sort((a, b) => b.cap - a.cap)

                caps.forEach(({stock_code}, i) => this.capitals[stock_code] = i)

            },
            onTreeMapMouseOver() {

            },
            onTreeMapMouseOut() {

            },
        },
        beforeDestroy() {
            console.log('beforeDestory')
            clearInterval(this.intervalTimer)
        },
}
</script>