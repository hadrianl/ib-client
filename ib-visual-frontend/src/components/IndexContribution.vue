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
import {InfluxDB} from 'influx'

export default {
        data() {
            return {
                // window: 0,
                influxclient: null,
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
            const host = 'localhost'
            const port = 8087
            const database = 'index_info'
            this.influxclient = new InfluxDB({host, port, database})
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
                // const query_last_sql = "show databases"
                const ret = await this.influxclient.query(query_last_sql)
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
                ret.forEach(({last, stock_name, time}) => {
                    treemap.data.push({name: stock_name, value: Math.abs(last), color: last>=0?'red':'green', time: time.toISOString(), y: last })
                })
                this.treemap_options.series = [treemap]
                // console.log(this.treemap_options)

            },
            async updateLine() {
                const sql = "select contribution from contribution where index_code='HSI' and time > now() - 6h group by stock_code, stock_name"
                const ret = await this.influxclient.query(sql)
                let series = []
                
                ret.groupRows.forEach(g => {
                    const stock_name = g.tags['stock_name']
                    const stock_code = g.tags['stock_code']
                    let line = {type: 'line', name: stock_name, data: [], visible: this.capitals[stock_code] < 10, id: stock_code, legendIndex: this.capitals[stock_code]}
                    g.rows.forEach(({time, contribution}) => line.data.push([time.getNanoTime()/1000000, contribution]))
                    series.push(line)
                    })
                this.line_options.series = series
                // console.log(this.line_options)

            },
            async getStockCapital() {
                const sql = "select last(capital) from stock_info group by stock_code, stock_name"
                let ret = await this.influxclient.query(sql)
                ret.sort((a, b) => b.last - a.last)

                ret.forEach(({stock_code}, i) => this.capitals[stock_code] = i)
                // console.log(this.capitals)
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