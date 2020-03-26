import Vue from 'vue'
import App from './App.vue'
import './plugins/view-design.js'
import IBWebsocket from './plugins/websocket.js'

Vue.config.productionTip = false
var ibws = new IBWebsocket('ws://localhost:6789')
Vue.$ibws = ibws
Vue.prototype.$ibws = ibws
window.ibws = ibws
// ibws.on('message', console.log)


new Vue({
  render: h => h(App),
}).$mount('#app')
