<template>
    <v-card>
        <v-tabs v-model="tab" grow slider-size="2" slider-color='blue'>
            <v-tab :key="1">{{$t('orderTab.stopLoss')}}</v-tab>
            <v-tab :key="2">{{$t('orderTab.maTrigger')}}</v-tab>
            <v-tab :key="3">{{$t('orderTab.trailStop')}}</v-tab>
            <v-tab :key="4">{{$t('orderTab.limit')}}</v-tab>
        </v-tabs>
        <!-- <v-tabs-slider></v-tabs-slider> -->
        <v-tabs-items v-model="tab">
            <v-tab-item :key="1">
                <StopLimitOrder />
            </v-tab-item>
            <v-tab-item :key="2">
                <MATriggerOrder />
            </v-tab-item>
            <v-tab-item :key="3">
                <TrailStopOrder />
            </v-tab-item>
            <v-tab-item :key="4">
                <LimitOrder />
            </v-tab-item>
        </v-tabs-items>
    </v-card>
</template>
<script>
import StopLimitOrder from './OrderTable/StopLimitOrder.vue'
import MATriggerOrder from './OrderTable/MATriggerOrder.vue'
import TrailStopOrder from './OrderTable/TrailStopOrder.vue'
import LimitOrder from './OrderTable/LimitOrder.vue'
export default {
    data() {
        return {
            tab: null
            // contractsList: [],
        }
    },
    components:{
        StopLimitOrder,
        MATriggerOrder,
        TrailStopOrder,
        LimitOrder,
    },
    mounted() {

    }
}
</script>
<style>

</style>