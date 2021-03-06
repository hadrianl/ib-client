<template>
      <v-data-table
        dense
        :headers="headers"
        :items="data"
        :loading="isloading"
        item-key="code"
        :expanded.sync="expanded"
        :height="400"
        fixed-header
        disable-pagination
        calculate-widths
        show-expand
        sort-by="upper_rate"
        sort-desc
        hide-default-footer
        class="elevation-1"
        >
        <template v-slot:expanded-item="{ headers, item }">
            <td :colspan="headers.length">
                <v-sheet v-ripple color="transparent" @click="showDetailChart(item.name, item.data)">
                <v-sparkline
                    :smooth="10"
                    :line-width="1"
                    :value="item.data.map(x => x.current)"
                    auto-draw
                    stroke-linecap="round"
                ></v-sparkline>
                </v-sheet>
                <v-dialog
                v-model="dialog"
                width="800"
                >
                    <highcharts :constructor-type="'stockChart'" :options="options"></highcharts>
                </v-dialog>
            </td>
        </template>
        <template v-slot:item.upper_rate="{ item }">
            <v-progress-linear 
            :value="item.upper_rate*100" 
            height="25"
            background-color="green accent-3"
            color="red accent-3"
            >{{ (item.upper_rate*100).toFixed(2) }}%</v-progress-linear>
        </template>
        <template v-slot:item.last_price="{ item }">
            <span
            :class="item.last_price>=item.avg_price?'red--text':'green--text'"
            >
                {{ item.last_price }}
            </span>
        </template>
        <template v-slot:item.percent="{ item }">
            <span
            :class="item.percent>=0?'red--text':'green--text'"
            >
                {{ item.percent }}%
            </span>
        </template>
        <template v-slot:item.code="{ item }">
            <a @click="$emit('select-code', item.code)">
                {{ item.code }}
            </a>
        </template>
        <template v-slot:top>
        <v-card>
            <v-toolbar 
            flat>
                <v-btn @click="refresh">
                    <v-icon>mdi-update</v-icon>
                    {{ lastUpatedTime?lastUpatedTime.toLocaleTimeString():"" }}
                </v-btn>
                <v-col cols="5">
                    <v-select 
                    label="index symbol" 
                    v-model="index_symbol" 
                    @change="refresh" 
                    :items="index_items"
                    hide-details="auto"
                    outlined
                    dense></v-select>
                </v-col>
                <v-spacer></v-spacer>
                <v-chip outlined label>Up Rate: <span :class="totalUpRate>=0.5?'red--text':'green--text'">{{ (totalUpRate*100).toFixed(2)}}</span> %</v-chip>
            </v-toolbar>
            <v-sheet>
            <v-sparkline
                :key="String(totalUpRate)"
                :value="upRateDistru"
                :gradient="['green', 'red']"
                :labels="['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']"
                gradient-direction="left"
                type="bar"
                auto-line-width
                auto-draw
                stroke-linecap="round"
            ></v-sparkline>
            </v-sheet>
            <!-- <div>{{upRateDistru}}</div> -->
        </v-card>
        </template>
    </v-data-table>
</template>
<script>
export default {
    data() {
        return {
            index_symbol: "",
            index_items: [],
            expanded: [],
            isloading: false,
            dialog: false,
            options: {
                chart: {
                    type: 'spline',
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
                xAxis: [
                    {type: 'datetime'},
                ],
                yAxis:[
                    {
                        title: 'price'
                    }
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
                                                verticalAlign: 'bottom',
                                        }
                                }
                        }]
                },
            },
            headers : [
                {
                    text: '', 
                    value: 'data-table-expand',
                },
                {
                    text: 'code',
                    value: 'code',
                    align: 'center',
                },
                {
                    text: 'name',
                    value: 'name',
                    align: 'center',
                },
                {
                    text: 'last price',
                    value: 'last_price',
                    align: 'center',
                },
                {
                    text: 'percent',
                    value: 'percent',
                    align: 'center',
                },
                {
                    text: 'upper rate',
                    value: 'upper_rate',
                    align: 'center',
                },
            ],
            data: [],
            upRateDistru: new Array(10).fill(0),
            totalUpRate: NaN,
            lastUpatedTime: undefined,
        }
    },
    created() {

    },
    async mounted() {
        console.log(this)
        await this.getIndexes()
        this.index_symbol = this.index_items[0]
    },
    computed: {
        // totalUpRate() {
        //     const upper = this.data.map(({last_price, avg_price}) => last_price >= avg_price)
        //     return upper?upper.reduce((p, c) => p + c, 0) / this.data.length:0
        // },
    },
    methods: {
        async refresh() {
            this.data = []
            this.upRateDistru.fill(0)

            if (!this.index_symbol) return
            
            this.isloading = true
            try{
                let ret = await this.axios.get('../extra/index/component', {params: {name: this.index_symbol}})
                let uppers = []
                Object.entries(ret.data).forEach(([code, {data: {items}, name}]) => {
                    const ur = items.filter(item => item.current>=item.avg_price).length/items.length
                    const last = items[items.length - 1].current
                    const avg = items[items.length - 1].avg_price
                    const pc = items[items.length - 1].percent

                    this.data.push({code: code, name: name, last_price: last, upper_rate: ur, avg_price: avg, percent: pc, data: items})

                    uppers.push(last > avg)

                    const ur_ = ur == 1?0.99:ur
                    this.upRateDistru[Math.floor(ur_*10)] += 1
                })

                this.totalUpRate = uppers.reduce((p, c) => p + c, 0) / uppers.length
                this.lastUpatedTime = new Date(ret.headers.date)
            }finally{
                this.isloading = false
            }
        
        },
        showDetailChart(name, data) {
            console.log(name)
            this.options.title.text = name

            this.options.series = [{name: name, data: data.map(({timestamp, current}) => [timestamp, current])}, {name: `${name}_avg`, data: data.map(({timestamp, avg_price}) => [timestamp, avg_price])}]
            this.dialog = true
            console.log(this.expanded)
        },
        async getIndexes() {
                const sql = `show tag values with key=index_code`
                const ret = await this.axios.get('../influxdb/query', {params: {q: sql, db: 'index_info'}})
                this.index_items = ret.data.results[0].series[0].values.map(x => x[1])
        },
    }
}
</script>