<template>
    <div class='legend' v-show="legend_bar.time">
        <div>Time: {{ new Date(legend_bar["time"] * 1000).toUTCString() }}</div>
        <div>Open: <strong>{{ legend_bar["open"] }}</strong></div>
        <div>High: <strong>{{ legend_bar["high"] }}</strong></div>
        <div>Low:  <strong>{{ legend_bar["low"] }}</strong></div>
        <div>close:  <strong>{{ legend_bar["close"] }}</strong></div>
        <div>volume: <strong>{{ legend_bar["volume"] }}</strong></div>
        <div>
            ma5:  <strong style="color:#DC143C;background:#D3D3D3">{{ legend_ma[5].toFixed(1) }}</strong> 
            ma10: <strong style="color:#FFFF00;background:#D3D3D3">{{ legend_ma[10].toFixed(1) }}</strong> 
            ma30: <strong style="color:#C0FF3E;background:#D3D3D3">{{ legend_ma[30].toFixed(1) }}</strong> 
            ma60: <strong style="color:#97FFFF;background:#D3D3D3">{{ legend_ma[60].toFixed(1) }}</strong>
        </div>
    </div>
</template>
<script>
export default {
    props: [
        'legend_bar',
        'legend_ma',
    ]
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