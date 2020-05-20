<template>
	<v-container fluid>
		<v-row justify="space-between" no-gutters>
			<v-col cols="8">
				<OrderManagementTab />
				<!-- <v-row align="stretch" justify="space-between" no-gutters>
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
				</v-row> -->
			</v-col>
			<v-divider inset vertical></v-divider>
			<v-col cols="3">
				<v-card>
					<OrderBook />
					<CostRef />
					<PlaceOrderTab />	
				</v-card>		
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
// import TradeTable from '../components/TradeTable.vue'
import PlaceOrderTab from '../components/PlaceOrderTab.vue'
// import PositionTable from '../components/PositionTable.vue'
// import PortfolioTable from '../components/PortfolioTable.vue'
import OrderBook from '../components/OrderBook.vue'
import CostRef from '../components/CostRef.vue'
import OrderManagementTab from '../components/OrderManagementTab.vue'

export default {
	components: {
		// PositionTable,
		// PortfolioTable,
		// TradeTable,
		OrderManagementTab,
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
