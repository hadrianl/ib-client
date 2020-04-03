import Vue from 'vue'
import App from './App.vue'
import './plugins/view-design.js'
import './plugins/echarts.js'
import IBWebsocket from './plugins/websocket.js'
import store from './store/store.js'
import echarts from 'echarts'

Vue.config.productionTip = false
var ibws = new IBWebsocket('ws://localhost:6789')
Vue.$ibws = ibws
Vue.prototype.$ibws = ibws
Vue.$echarts = echarts
Vue.prototype.$echarts = echarts
window.ibws = ibws
// ibws.on('message', console.log)

new Vue({
  store,
  mounted() {
    var _this = this
		this.$ibws.on('error', function(e) {
			_this.$Notice.error({
				title: 'Error',
				desc: e,
			})
		})

		this.$ibws.on('open', function(d) {
			_this.$store.commit('setConnectState', true)
			_this.$Message.success({
				background: true,
				content: "连接已成功" + this.url + ',' + d.msg,
			})
		})

		this.$ibws.on('close', function() {
			_this.$store.commit('setConnectState', false)
			_this.$Message.warning({
				background: true,
				content: "连接已断开",
			})
		})

		this.$ibws.on('death', function(d) {
			_this.$Message.error({
				background: true,
				content: d.msg + ",请刷新页面重新创建连接",
				duration: 0
			})
		})

		this.$ibws.on('connect_sync', function(){
			console.log('connect_sync')
			_this.$ibws.send({'action': "get_all_trades"})
			_this.$ibws.send({'action': "get_all_positions"})
		})
  },
  render: h => h(App),
}).$mount('#app')
