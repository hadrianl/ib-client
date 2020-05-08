import Vue from 'vue'
import App from './App.vue'
// import './plugins/view-design.js'
// import './plugins/echarts.js'
import './plugins/eventBus.js'
import ibws from './plugins/websocket.js'
import store from './store/store.js'
import router from './router/router.js'
// import echarts from 'echarts'
import vuetify from './plugins/vuetify.js'

Vue.config.productionTip = false
// var ibws = new IBWebsocket('ws://localhost:6789')
// Vue.$ibws = ibws
// Vue.prototype.$ibws = ibws
window.ibws = ibws
// window.onload = function(){
//     //去掉默认的contextmenu事件，否则会和右键事件同时出现。
//     document.oncontextmenu = function(e){
//         e.preventDefault();
//     }
// }

const vm = new Vue({
    store,
    router,
    mounted() {
        var _this = this

        this.$ibws.on('open', function() {
            _this.$store.commit('setConnectState', true)
        })

        this.$ibws.on('close', function() {
            _this.$store.commit('setConnectState', false)
        })

        this.$ibws.on('connect_sync', function(){
            _this.$ibws.send({'action': "get_all_trades"})
            _this.$ibws.send({'action': "get_all_positions"})
            _this.$ibws.send({'action': "get_all_fills"})
        })

        this.$ibws.on('trades', function (ts) {
            _this.$store.commit('initTrades', ts)
        })
        
        this.$ibws.on('trade', function (t) {
            _this.$store.commit('updateTrade', t) 
        })
        
        this.$ibws.on('positions', function (ps) {
            _this.$store.commit('initPositions', ps)
        })
        
        this.$ibws.on('position', function (p) {
            _this.$store.commit('updatePosition', p)
            
        })
        
        this.$ibws.on('fills', function (fs) {
            _this.$store.commit('initFills', fs)
            
        })
        
        this.$ibws.on('fill', function (f) {
            _this.$store.commit('updateFill', f)
            
        })
    },
    vuetify,
    render: h => h(App)
}).$mount('#app')

window.vm = vm