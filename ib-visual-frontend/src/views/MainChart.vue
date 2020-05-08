<template>
	<v-container class='mt-1 pt-1'>
		<v-row align="stretch" justify="space-between" no-gutters>
			<v-col cols="8">
				<v-row>
					<TradeTable height="400"/>
				</v-row>
				<v-divider :inset="false"></v-divider>
				<v-row>
					<PositionTable height="200"/>
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
import OrderBook from '../components/OrderBook.vue'
import CostRef from '../components/CostRef.vue'

export default {
	components: {
		PositionTable,
		TradeTable,
		PlaceOrderTab,
		OrderBook,
		CostRef,
		},
	computed: {

	},
	data(){
		return {
			lr: 0.78,
			tb: 0.7
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
