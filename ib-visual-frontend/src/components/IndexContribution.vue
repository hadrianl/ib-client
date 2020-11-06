<template>
    <v-container fluid>
        <v-row justify="space-between" no-gutters>
            <v-col cols="8">
                <highcharts :constructor-type="'stockChart'" :options="line_options"></highcharts>
            </v-col>
            <v-col cols="4">
                <highcharts :options="treemap_options"></highcharts>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import {InfluxDB} from 'influx'

export default {
        data() {
            return {
                influxclient: null,
                line_options: {
                    title: {
                        text: 'HSI贡献度趋势',
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
                    // xAxis: [
                    //     {type: 'datetime'},
                    // ],
                    tooltip: {
                        split: false,
                    },
                    series: [],
                },
                treemap_options: {
                    title: {
                        text: 'HSI贡献度热力图',
                    },
                    xAxis: [
                        {type: 'datetime'},
                    ],
                    series: [],
                },
                intervalTimer: null,
            }
        },
        async mounted() {
            console.log('indecContribution mounted')
            this.influxclient = new InfluxDB({host: 'localhost', port: 8087, database: 'index_info'})
            await this.updateLine()
            await this.updateHeatMap()
            this.intervalTimer = setInterval(async () => {
                await this.updateLine()
                await this.updateHeatMap()
            }, 60000)

        },
        methods: {
            async updateHeatMap() {
                console.log('updateHeatMap')
                const query_last_sql = "select last(contribution) from contribution where index_code='HSI' group by stock_code, stock_name"
                // const query_last_sql = "show databases"
                const ret = await this.influxclient.query(query_last_sql)
                let treemap = {
                        type: "treemap",
                        name: "HSI",
                        layoutAlgorithm: 'squarified',
                        alternateStartingDirection: true,
                        title: 'test',
                        pointPadding: 3,
                        data: [],
                    }
                ret.forEach(({last, stock_name, stock_code}) => treemap.data.push({name: stock_name, value: Math.abs(last), color: last>=0?'red':'green', drilldown: stock_code }))
                this.treemap_options.series = [treemap]
                console.log(this.treemap_options)

            },
            async updateLine() {
                const sql = "select contribution from contribution where index_code='HSI' and time > now() - 6h group by stock_code, stock_name"
                const ret = await this.influxclient.query(sql)
                let series = []
                
                ret.groupRows.forEach(g => {
                    let line = {type: 'line', name: g.tags['stock_name'], data: [], visible: true, id: g.tags['stock_code']}
                    g.rows.forEach(({time, contribution}) => line.data.push([time.getNanoTime()/1000000, contribution]))
                    series.push(line)
                    })
                this.line_options.series = series
                console.log(this.line_options)

            }
        },
        beforeDestroy() {
            console.log('beforeDestory')
            clearInterval(this.intervalTimer)
        },
}
</script>