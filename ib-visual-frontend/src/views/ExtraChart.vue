<template>
    <v-list>
        <v-list-item-group>
            <v-list-item v-for="[code, name, data] in values" :key="code">
                <v-list-item-content>
                    <v-card
                        class="mx-auto"
                        color="grey lighten-4"
                        max-width="600"
                    >
                        <v-card-title>
                        <v-row align="start">
                            <div class="font-weight-black">
                            {{ name }}
                            </div>
                            <v-spacer></v-spacer>
                            <div class="caption grey--text text-uppercase">
                            Last Price:
                            </div>
                            <div>
                            <span
                                class="font-weight-black"
                                v-text="data[data.length - 1][1]"
                            ></span>
                            <!-- <strong v-if="avg">BPM</strong> -->
                            </div>
                        </v-row>
                        <v-spacer></v-spacer>
                        <v-btn
                            icon
                            class="align-self-start"
                            size="28"
                            @click="showDetailChart(name, data)"
                        >
                            <v-icon>mdi-arrow-up-thick</v-icon>
                        </v-btn>
                        </v-card-title>

                        <v-sheet color="transparent">
                        <v-sparkline
                            :smooth="10"
                            :line-width="1"
                            :value="data.map(x => x[1])"
                            auto-draw
                            stroke-linecap="round"
                        ></v-sparkline>
                        </v-sheet>
                    </v-card>
                </v-list-item-content>
            </v-list-item>
        </v-list-item-group>
        <v-dialog
        v-model="dialog"
        width="800"
        >
            <!-- <v-card>
                <v-card-text> -->
                    <highcharts :constructor-type="'stockChart'" :options="options"></highcharts>
                <!-- </v-card-text>
            </v-card> -->
        </v-dialog>
    </v-list>
</template>
<script>
export default {
    data() {
        return {
            values: [],
            dialog: false,
            options: {
                global: {
                    timezoneOffset: 8 * 60,
                },
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
        }
    },
    created() {

    },
    mounted() {
        this.refresh()
        console.log(this.values)
    },
    methods: {
        refresh: async function() {
            let ret = await this.axios.get('../extra/index/component', {"name": "HSI"})
            console.log(ret)
            this.values = []
            Object.entries(ret.data).forEach(([code, {data: {items}, name}]) => {
                this.values.push([code, name, items.map(item => [item.timestamp, item.current, item.avg_price])])
            })
        },
        showDetailChart(name, data) {
            this.options.title.text = name
            // this.options.xAxis.breaks = {
            //     breakSize: 3600000,
            //     from: data[0][0] + 1000*60*60*2.5
            // }

            this.options.series = [{name: name, data: data.map(x => x.slice(0, 2))}, {name: `${name}_avg`, data: data.map(x => [x[0], x[2]])}]
            this.dialog = true
        }
    }
}
</script>