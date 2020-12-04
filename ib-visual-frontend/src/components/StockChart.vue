<template>
    <v-card @keyup.enter="updateChart">
        <v-toolbar color="indigo" dark dense class="d-flex justify-space-between">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-autocomplete
                    label="symbol"
                    v-model="symbol"
                    :items="itemsList"
                    :search-input.sync="search"
                    item-text= "name"
                    item-value="code"
                    :loading="searchloading"
                    auto-select-first
                    outlined
                    dense
                    clearable
                    hide-no-data
                    placeholder="enter symbol"
                    hide-details="auto"
                    v-bind="attrs"
                    v-on="on"
                    ></v-autocomplete>
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
            symbolList: [],
            search: null,
            searchloading: false,
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
                },
                credits: {
                    enabled: false,
                    },
                legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'middle'
                },
                yAxis:[
                    {
                        height: '80%',
						resize: {
							enabled: true
						},
                        lineWidth: 0
                    }, 
                    {
						top: '80%',
						height: '20%',
						offset: 0,
                        lineWidth: 0
                    }
                    ],
                series: [
                    {
						type: 'candlestick',
						name: '',
						color: 'green',
						lineColor: 'green',
						upColor: 'red',
						upLineColor: 'red',
						data: [],
                    },
                    {
                        type: 'column',
                        name: 'volume',
                        data: [],
                        yAxis: 1,
                    }
                    ],
            },
        }
    },
    methods: {
        async updateChart() {
            console.log(this.symbol)
            this.$refs.sc.chart.showLoading()
            try{
                const params = {
                    code: this.symbol,
                    begin: Date.now(),
                    count: -this.barCount,
                    period: this.period,
                }
                const ret = await this.axios.get('../extra/stock/kline', {params})
                
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
            }finally{
                this.$refs.sc.chart.hideLoading()
            }
            
        }
    },
    computed: {
        itemsList() {
            return this.symbolList.map(({code, name}) => ({code, name:`${name}(${code})`}))
        }
    },
    watch: {
        async search(code) {
            if (!code) {
                this.symbolList =[]
                return
            }

            this.searchloading = true
            try{
                const params = {code: code, size: 50}
                const ret = await this.axios.get('../extra/stock/search', {params})
                    
                this.symbolList = ret.data.stocks || []
            }finally{
                this.searchloading = false
            }
        }
    }
}
</script>