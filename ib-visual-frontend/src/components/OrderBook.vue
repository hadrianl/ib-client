<template>
    <v-container>
        <h4 class="grey--text text--darken-1 text-center">{{ ticker.time }}</h4>
        <v-progress-linear v-model="askSizeRate" color='#00FF7F'></v-progress-linear>
        <v-btn color='#90EE90' block @click="attachPriceClick(ticker.ask)">{{ askLabel }}</v-btn>
        <v-btn color='#ADD8E6' block @click="attachPriceClick(ticker.last)">{{ lastLabel }}</v-btn>
        <v-btn color='#F08080' block @click="attachPriceClick(ticker.bid)">{{ bidLabel }}</v-btn>
        <v-progress-linear v-model="bidSizeRate" color='#FF6347'></v-progress-linear>
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
    inject: [
        "setOrderBaseOnAttachPrice"
    ],
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
        },
        askSizeRate() {
            return this.ticker.askSize / (this.ticker.askSize + this.ticker.bidSize) * 100
        },
        bidSizeRate() {
            return this.ticker.bidSize / (this.ticker.askSize + this.ticker.bidSize) * 100
        },
    },
    watch: {
        contract(newCon, oldCon) {
            if (oldCon) {
                this.$ibws.send({'action': 'unsub_ticker', 'contract': oldCon})
            }

            if (newCon) {
                this.$ibws.send({'action': 'sub_ticker', 'contract': newCon})
            }
            
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
            // this.$bus.$emit('attachPrice', price)
            this.setOrderBaseOnAttachPrice(price)
            // this.$emit('attach-price', price)
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