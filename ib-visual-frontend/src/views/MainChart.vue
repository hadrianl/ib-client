<template>
	<v-container fluid>
		<v-row justify="space-between" no-gutters>
			<v-col cols="8">
				<OrderManagementTab />
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
