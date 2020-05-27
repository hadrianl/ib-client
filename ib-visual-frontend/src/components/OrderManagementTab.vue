<template>
    <v-card>
        <v-tabs v-model="tab" slider-size="2" slider-color='blue'>
            <v-tab :key="1">{{$t('mainTab.order')}}</v-tab>
            <v-tab :key="2">{{$t('mainTab.fill')}}</v-tab>
            <v-tab :key="3">{{$t('mainTab.portfolio')}}</v-tab>
            <v-tab :key="4">{{$t('mainTab.position')}}</v-tab>
        </v-tabs>
        <!-- <v-tabs-slider></v-tabs-slider> -->
        <v-tabs-items v-model="tab">
            <v-tab-item :key="1">
                <TradeTable height="350"/>
            </v-tab-item>
            <v-tab-item :key="2">
                <FillTable height="350" />
            </v-tab-item>
            <v-tab-item :key="3">
                <PortfolioTable height="350"/>
            </v-tab-item>
            <v-tab-item :key="4">
                <PositionTable height="350"/>
            </v-tab-item>
        </v-tabs-items>
    </v-card>
</template>
<script>
import TradeTable from './TradeTable.vue'
import PortfolioTable from './PortfolioTable.vue'
import PositionTable from './PositionTable.vue'
import FillTable from './FillTable.vue'
export default {
    data() {
        return {
            tab: null
            // contractsList: [],
        }
    },
    components:{
        TradeTable,
        FillTable,
        PortfolioTable,
        PositionTable,
    },
}
</script>