import Vue from 'vue'
import App from './App.vue'
import './plugins/eventBus.js'
import './plugins/highcharts.js'
import ibws from './plugins/websocket.js'
import i18n from './plugins/i18n.js'
import store from './store/store.js'
import router from './router/router.js'
import vuetify from './plugins/vuetify.js'

Vue.config.productionTip = false
window.ibws = ibws
console.log(process.env.APIURL)
console.log(router)

const vm = new Vue({
    store,
    router,
    i18n,
    mounted() {
        this.$ibws.on('open', () => {
            this.$store.commit('setConnectState', true)
        })

        this.$ibws.on('close', () => {
            this.$store.commit('setConnectState', false)
        })

        this.$ibws.on('connect_sync', () => {
            this.$ibws.send({'action': "get_all_trades"})
            this.$ibws.send({'action': "get_all_portfolio"})
            this.$ibws.send({'action': "get_all_positions"})
            this.$ibws.send({'action': "get_all_fills"})
            this.$ibws.send({'action': "get_all_account_values"})
        })

        this.$ibws.on('trades', (ts) => {
            this.$store.commit('initTrades', ts)
        })
        
        this.$ibws.on('trade', (t) => {
            this.$store.commit('updateTrade', t) 
        })
        
        this.$ibws.on('positions', (ps) => {
            this.$store.commit('initPositions', ps)
        })
        
        this.$ibws.on('position', (p) => {
            this.$store.commit('updatePosition', p)
        })

        this.$ibws.on('portfolio', (pf) => {
            this.$store.commit('initPortfolio', pf)
        })
        
        this.$ibws.on('portfolioItem', (pfi) => {
            this.$store.commit('updatePortfolio', pfi)
        })
        
        this.$ibws.on('fills', (fs) => {
            this.$store.commit('initFills', fs)   
        })
        
        this.$ibws.on('fill', (f) => {
            this.$store.commit('updateFill', f)
        })

        this.$ibws.on('account_values', (avs) => {
            this.$store.commit('initAccountValues', avs)
        })

        this.$ibws.on('account_value', (av) => {
            this.$store.commit('updateAccountValue', av)
        })
    },
    vuetify,
    render: h => h(App)
}).$mount('#app')

window.vm = vm