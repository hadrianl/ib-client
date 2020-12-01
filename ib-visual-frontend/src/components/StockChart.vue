<template>
    <v-card @keyup.enter="updateChart">
        <v-toolbar color="indigo" dark dense class="d-flex justify-space-between">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                    label="symbol"
                    v-model="symbol"
                    outlined
                    dense
                    clearable
                    validate-on-blur
                    placeholder="enter symbol"
                    hide-details="auto"
                    v-bind="attrs"
                    v-on="on"
                    ></v-text-field>
                </template>
                <span>输入股票代码如：00700, SH601012, SZ002609</span>
            </v-tooltip>
            <v-text-field
                label="count"
                v-model="barCount"
                outlined
                dense
                validate-on-blur
                hide-details="auto"
                placeholder="bar length"
                type="number"
            ></v-text-field>
            <v-select
            v-model="period"
            :items="periods"
            label="period"
            dense
            outlined
            hide-details="auto"
            ></v-select>
        </v-toolbar>
        <highcharts ref="sc" :constructor-type="'stockChart'" :options="options"></highcharts>
    </v-card>
</template>
<script>
export default {
    data() {
        return {
            symbol: "",
            barCount: 284,
            period: "1m",
            periods: [
                "1m",
                "5m",
                "10m",
                "15m",
                "30m",
                "60m",
                "120m",
                "day",
                "week",
                "month",
                "quarter",
                "year"
            ],
            options: {
                chart: {
                    type: 'candlestick',
                },
                title: {
                    text: '',
                },
                rangeSelector: {
                    enabled: false,
                    buttons: [
                        {
                            type: 'minute',
                            count: 60,
                            text: '1h',
                        }, 
                        {
                            type: 'minute',
                            count: 120,
                            text: '2h',
                        }, 
                        {
                            type: 'all',
                            text: 'All',
                        },
                    ],
                },
                credits: {
                    enabled: false,
                    },
                legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle'
                },
                yAxis:[{

						height: '65%',
						resize: {
								enabled: true
						},
						lineWidth: 0
				}, {
						top: '65%',
						height: '35%',
						offset: 0,
						lineWidth: 0
				}],
                series: [
                    {
						type: 'candlestick',
						name: '',
						color: 'green',
						lineColor: 'green',
						upColor: 'red',
						upLineColor: 'red',
						data: [],
				},{
						type: 'column',
						data: [],
						yAxis: 1,
				}
                ],
            },
        }
    },
    methods: {
        async updateChart() {
            this.$refs.sc.chart.showLoading()
            const params = {
                code: this.symbol,
                begin: Date.now(),
                count: -this.barCount,
                period: this.period,
            }
            const ret = await this.axios.get('../extra/stock/kline', {params})
            this.$refs.sc.chart.hideLoading()
            console.log(ret)

            const result = ret.data

            if (result.error_code != 0) throw result.error_description

            // this.options.title.text = `${this.symbol}`
            this.options.series[0].name = `${result.data.symbol}`
            this.options.series[0].data = []
            this.options.series[1].data = []

            result.data.item.forEach(([timestamp, volume, open, high, low, close]) => {
                this.options.series[0].data.push([timestamp, open, high, low, close])
                this.options.series[1].data.push([timestamp, volume])
            })
        }
    },
    // watch: {
    //     symbol(nv) {
    //         console.log(nv)
    //     }
    // }
}
</script>