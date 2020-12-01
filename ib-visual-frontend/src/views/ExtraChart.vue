<template>
	<v-container fluid>
		<v-row justify="space-between" no-gutters>
            <v-col cols="4">
                <UpperRate @select-code="selectCode"/>
			</v-col>
            <v-divider inset vertical></v-divider>
            <v-col cols="7">
                <StockChart ref="stockchart" />
            </v-col>
        </v-row>
	</v-container>
</template>
<script>
import UpperRate from '../components/UpperRate.vue'
import StockChart from '../components/StockChart.vue'
export default {
    components: {
        UpperRate,
        StockChart
    },
    methods: {
        selectCode(code) {
            this.$refs.stockchart.symbol = code
            this.$refs.stockchart.updateChart()
        }
    }
}
</script>