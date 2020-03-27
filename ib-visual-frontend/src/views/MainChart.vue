<template>
    <div id="main-chart">
		<!-- <Alert v-if="!isReady" type="error">未连接，请重新刷新页面或检查后端时候已连接</Alert> -->
        <SplitLeftRight :split="0.8">
            <template slot="left">
                <TradeTable :height="450" />
            </template>
            <template slot="right">
                <PlaceOrderTab name="name1"/>
            </template>
        </SplitLeftRight>
    </div>
</template>

<script>
import TradeTable from '../components/TradeTable.vue'
import SplitLeftRight from '../components/SplitLeftRight.vue'
import PlaceOrderTab from '../components/PlaceOrderTab.vue'

export default {
	components: {
		SplitLeftRight,
		TradeTable,
		PlaceOrderTab
		},
	computed: {
		// isReady() {
		// 		return this.$ibws.isReady()
		// 	}
		},
	beforeCreate: () => {
		// 在实例初始化之后，数据观测 (data observer) 和 event/watcher 事件配置之前被调用。
	},
	created: () => {
		// 在实例创建完成后被立即调用。在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。然而，挂载阶段还没开始，$el 属性目前不可见。
	},
	beforeMount: () => {
		// 在挂载开始之前被调用：相关的 render 函数首次被调用。
	},
	mounted: function () {
		var _this = this
		this.$ibws.on('error', function(e) {
			_this.$Notice.error({
				title: 'Error',
				desc: e,
			})
		})

		this.$ibws.on('open', function(d) {
			_this.$Notice.success({
				title: 'Connection',
				desc: '连接' + this.url + ',' + d.msg,
			})
		})

		this.$ibws.on('close', function() {
			_this.$Notice.warning({
				title: 'Connection',
				desc: '连接断开',
			})
		})

		this.$ibws.on('death', function(d) {
			_this.$Notice.error({
				title: 'Connection Failed!',
				desc: d.msg,
				duration: 0
			})
		})
		
		this.$ibws.init(false)
		this.$ibws.send({'action': "get_all_trades"})
	},
	beforeUpdate: () => {
		// 数据更新时调用，发生在虚拟 DOM 打补丁之前。这里适合在更新之前访问现有的 DOM，比如手动移除已添加的事件监听器。
	},
	updated: () => {
		// 由于数据更改导致的虚拟 DOM 重新渲染和打补丁，在这之后会调用该钩子。
		// 当这个钩子被调用时，组件 DOM 已经更新，所以你现在可以执行依赖于 DOM 的操作。然而在大多数情况下，你应该避免在此期间更改状态。如果要相应状态改变，通常最好使用计算属性或 watcher 取而代之。
		// 注意 updated 不会承诺所有的子组件也都一起被重绘。
	},
	activated: () => {
		// keep-alive 组件激活时调用。
	},
	deactivated: () => {
		// keep-alive 组件停用时调用。
	},
	beforeDestroy: () => {
		// 实例销毁之前调用。在这一步，实例仍然完全可用。
	},
	destroyed: () => {
		// Vue 实例销毁后调用。调用后，Vue 实例指示的所有东西都会解绑定，所有的事件监听器会被移除，所有的子实例也会被销毁。
	},
}
</script>

<style>
#main-chart {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
