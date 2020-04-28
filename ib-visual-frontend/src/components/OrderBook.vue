<template>
    <v-container>
        <v-row><v-btn :value="ticker.ask" color='green' block @click="attachPriceClick(ticker.ask)">ASK:{{ ticker.askSize }}@{{ ticker.ask }}</v-btn></v-row>
        <v-row><v-btn :value="ticker.last" color='blue' block @click="attachPriceClick(ticker.last)">LAST:{{ ticker.lastSize }}@{{ ticker.last }}</v-btn></v-row>
        <v-row><v-btn :value="ticker.bid" color='red' block @click="attachPriceClick(ticker.bid)">BID:{{ ticker.bidSize }}@{{ ticker.bid }}</v-btn></v-row>
    </v-container>
</template>
<script>
export default {
    data() {
        return {
            attachPrice: NaN,
            ticker: {bid: NaN, ask: NaN, last: NaN, bidSize: NaN, askSize: NaN, lastSize: NaN, time: "", conId: NaN}
        }
    },
    computed: {
        contract() {
            return this.$store.state.currentContract
        },
        askLabel() {
            return `ASK: ${this.ticker.askSize}@${this.ticker.ask}`
        },
        lastLabel() {
            return `LAST: ${this.ticker.lastSize}@${this.ticker.last}`
        },
        bidLabel() {
            return `BID: ${this.ticker.bidSize}@${this.ticker.bid}`
        }
    },
    watch: {
        contract(newCon, oldCon) {
            if (oldCon) {
                this.$ibws.send({'action': 'unsub_ticker', 'contract': oldCon})
            }

            this.$ibws.send({'action': 'sub_ticker', 'contract': newCon})
        },
    },
    mounted() {
        this.$ibws.on('ticker', this.handleTicker)
        if(this.contract) {
            this.$ibws.send({'action': 'sub_ticker', 'contract': this.contract})
        }
    },
    methods: {
        handleTicker(ticker) {
            Object.assign(this.ticker, ticker)
        },
        attachPriceClick(price) {
            this.$bus.$emit('attachPrice', price)
        }
    },
    beforeDestroy() {
        if (this.contract) {
            this.$ibws.send({'action': 'unsub_ticker', 'contract': this.contract})
        }  
        this.$ibws.off('ticker', this.handleTicker)
	},
    
}
</script>