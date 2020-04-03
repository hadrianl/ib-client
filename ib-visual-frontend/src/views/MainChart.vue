<template>
    <div id="main-chart" class="split">
		<!-- <Alert v-if="!isReady" type="error">未连接，请重新刷新页面或检查后端时候已连接</Alert> -->
		<Split v-model="lr">
            <div slot="left" class="split-pane no-padding">
				<Split v-model="tb" mode="vertical">
					<div slot="top" class="split-pane">
						<TradeTable />
					</div>
					<div slot="bottom" class="split-pane">
						<PositionTable />
					</div>
				</Split>
                
            </div>
            <div slot="right" class="split-pane">
				<ContractItem></ContractItem>
                <PlaceOrderTab name="name1"/>
            </div>
        </Split>
    </div>
</template>

<script>
import TradeTable from '../components/TradeTable.vue'
import PlaceOrderTab from '../components/PlaceOrderTab.vue'
import PositionTable from '../components/PositionTable.vue'
import ContractItem from '../components/ContractItem.vue'

export default {
	components: {
		ContractItem,
		PositionTable,
		TradeTable,
		PlaceOrderTab,
		// BarChart,
		},
	computed: {
		// contract: function() {
		// 	return this.$refs.contract.currentContract
		// }
	},
	data(){
		return {
			lr: 0.78,
			tb: 0.7
		}
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
	/* font-family: Avenir, Helvetica, Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px; */
	}

    .split{
        /* height: 200px; */
        border: 1px solid #dcdee2;
    }
    .split-pane{
        padding: 10px;
    }
    .split-pane.no-padding{
        height: 450px;
        padding: 0;
    }
</style>
