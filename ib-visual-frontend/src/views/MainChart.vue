<template>
	<v-container class='ma-auto pa-auto' justify="space-between">
		<v-row align="stretch" justify="space-between" no-gutters>
			<v-col cols="8">
				<v-row>
					<TradeTable height="400"/>
				</v-row>
				<v-divider :inset="false"></v-divider>
				<v-row align="stretch" justify="space-between" no-gutters>
					<v-col cols="8">
						<PortfolioTable height="200" />
					</v-col>
					<v-col cols="4">
						<PositionTable height="200" />
					</v-col>
				</v-row>
			</v-col>
			<v-divider :inset="false" vertical></v-divider>
			<v-col cols="3">
				<OrderBook />
				<CostRef />
				<PlaceOrderTab />	
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import TradeTable from '../components/TradeTable.vue'
import PlaceOrderTab from '../components/PlaceOrderTab.vue'
import PositionTable from '../components/PositionTable.vue'
import PortfolioTable from '../components/PortfolioTable.vue'
import OrderBook from '../components/OrderBook.vue'
import CostRef from '../components/CostRef.vue'

export default {
	components: {
		PositionTable,
		PortfolioTable,
		TradeTable,
		PlaceOrderTab,
		OrderBook,
		CostRef,
		},
	computed: {

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
