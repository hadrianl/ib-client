<template>
	<v-container fluid>
		<v-row justify="space-between" no-gutters>
			<v-col cols="8">
				<OrderManagementTab />
			</v-col>
			<v-divider inset vertical></v-divider>
			<v-col cols="3">
				<v-card>
					<OrderBook ref="ob"/>
					<CostRef />
					<PlaceOrderTab ref="ot"/>	
				</v-card>		
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import PlaceOrderTab from '../components/PlaceOrderTab.vue'
import OrderBook from '../components/OrderBook.vue'
import CostRef from '../components/CostRef.vue'
import OrderManagementTab from '../components/OrderManagementTab.vue'

export default {
	components: {
		OrderManagementTab,
		PlaceOrderTab,
		OrderBook,
		CostRef,
		},
	computed: {

	},
	methods: {
		setOrderBaseOnCost(cost) {
			this.$refs.ot.setOrderBaseOnCost(cost)
		},
		setOrderBaseOnAttachPrice(price) {
			this.$refs.ot.setOrderBaseOnAttachPrice(price)
		},
		getCurrentTicker() {
			return this.$refs.ob.ticker
		}
	},
	provide() {
		return {
			setOrderBaseOnCost : this.setOrderBaseOnCost,
			setOrderBaseOnAttachPrice: this.setOrderBaseOnAttachPrice,
			getCurrentTicker: this.getCurrentTicker,
		}
	},
	data(){
		return {
		}
		},	
	beforeCreate() {
		
	},
	created() {
		
	},
	beforeMount() {
		
	},
	mounted() {

	},
	beforeUpdate() {
		
	},
	updated() {
		
	},
	activated() {
		
	},
	deactivated() {
		
	},
	beforeDestroy() {
		
	},
	destroyed() {
		
	},
}
</script>

<style>

</style>
