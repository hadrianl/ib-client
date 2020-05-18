<template>
    <div class='legend' v-show="legend_bar.time">
        <div style="color:#FFFFFF">Time: {{ new Date(legend_bar["time"] * 1000).toUTCString() }}</div>
        <div style="color:#FFFFFF">Open:   <strong :style="ohlcLegendStyle">{{ legend_bar["open"] }}</strong></div>
        <div style="color:#FFFFFF">High:   <strong :style="ohlcLegendStyle">{{ legend_bar["high"] }}</strong></div>
        <div style="color:#FFFFFF">Low:    <strong :style="ohlcLegendStyle">{{ legend_bar["low"] }}</strong></div>
        <div style="color:#FFFFFF">Close:  <strong :style="ohlcLegendStyle">{{ legend_bar["close"] }}</strong></div>
        <div style="color:#FFFFFF">Volume: <strong :style="ohlcLegendStyle">{{ legend_bar["volume"] }}</strong></div>
        <div style="color:#FFFFFF">
            <inline v-for="(v, p) in legend_ma" :key="p" :name="p">
                ma{{p}}: <strong :style="maStyles[p]">{{ v?v.toFixed(1):v }}</strong> 
            </inline>
        </div>    
    </div>
</template>
<script>
export default {
    data() {
        return {
            ohlcLegendStyle: {
                color: "#FFFFFFF",
                background: "#FF8C00"
            },
            maStyles: {
                5:  {
                    color: "#DC143C",
                    // background: "#696969",
                },
                10: {
                    color: "#FFC125",
                    // background: "#696969",
                },
                30: {
                    color: "#C0FF3E",
                    // background: "#696969",
                },
                60: {
                    color: "#97FFFF",
                    // background: "#696969",
                },
            }
        }
    },
    props: [
        'legend_bar',
        'legend_ma',
    ],
}
</script>
<style lang="scss">
    .legend {
    position: absolute;
    top: 1em;
    left: 1em;
    font-family: Roboto Condensed;
    z-index: 2;
    opacity: .1;
    transition: opacity .2s cubic-bezier(0.005, 1, 0.22, 1);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    }
</style>