<template>
    <div :class="className" :id="id" :style="styleObject" :option="option"> </div>
</template>
<script>
import echarts from "echarts"
export default {
    props: {
        className: {
            type: String,
            default: "",
            },
        id: String,
        styleObject: {
            height: {
                type: String,
                default: "auto",
            },
            width: {
                type: String,
                default: "auto",
            }
        },
        option: Object,
    },
    data() {
        return {
            chart: null
        }
    },

    mounted() {
        this.chart = this.$echart.init(document.getElementById(this.id))
        this.chart.setOption(this.option)
    }
}
</script>