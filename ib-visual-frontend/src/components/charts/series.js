export default {
    ohlc: {
        type: 'Candlestick',
        options: {
            upColor: '#FF0000',
            downColor: '#00FFFF',
            borderVisible: false,
            wickVisible: true,
            // borderColor: '#000000',
            wickColor: '#FFFFFF',
            // borderUpColor: '#4682B4',
            // borderDownColor: '#A52A2A',
            // wickUpColor: "#4682B4",
            // wickDownColor: "#A52A2A",
            scaleMargins: {
                top: 0.1,
                bottom: 0.3
            }
        },
    },
    vol: {
        type: 'Histogram',
        options: {
            base: 0, 
            overlay: true,
            color: '#6495ED',
            scaleMargins: {
                top: 0.6,
                bottom: 0.02
            }
        },
    }
}