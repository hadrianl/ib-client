<template>
    <v-card>
        <v-tabs v-model="tab" grow slider-size="2" slider-color='blue'>
            <v-tab :key="0">{{$t('orderTab.stopLoss')}}</v-tab>
            <v-tab :key="1">{{$t('orderTab.maTrigger')}}</v-tab>
            <v-tab :key="2">{{$t('orderTab.trailStop')}}</v-tab>
            <v-tab :key="3">{{$t('orderTab.limit')}}</v-tab>
            <v-tab :key="4">{{$t('orderTab.bracket')}}</v-tab>
        </v-tabs>
        <!-- <v-tabs-slider></v-tabs-slider> -->
        <v-tabs-items v-model="tab">
            <v-tab-item :key="0">
                <StopLimitOrder ref="sl"/>
            </v-tab-item>
            <v-tab-item :key="1">
                <MATriggerOrder />
            </v-tab-item>
            <v-tab-item :key="2">
                <TrailStopOrder ref="ts"/>
            </v-tab-item>
            <v-tab-item :key="3">
                <LimitOrder ref="l"/>
            </v-tab-item>
            <v-tab-item :key="4">
                <BracketOrders ref="b"/>
            </v-tab-item>
        </v-tabs-items>
    </v-card>
</template>
<script>
import StopLimitOrder from './OrderTable/StopLimitOrder.vue'
import MATriggerOrder from './OrderTable/MATriggerOrder.vue'
import TrailStopOrder from './OrderTable/TrailStopOrder.vue'
import LimitOrder from './OrderTable/LimitOrder.vue'
import BracketOrders from './OrderTable/BracketOrders.vue'
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
        BracketOrders,
    },
    methods: {
        setOrderBaseOnCost(cost){
            switch (this.tab) {
            case 0:
                this.$refs.sl.setOrderBaseOnCost(cost)
                break
            case 2:
                this.$refs.ts.setOrderBaseOnCost(cost)
                break
            case 3:
                this.$refs.l.setOrderBaseOnCost(cost)
                break
            case 4:
                this.$refs.b.setOrderBaseOnCost(cost)
                break
            }
        },
        setOrderBaseOnAttachPrice(price) {
            switch (this.tab) {
            case 0:
                this.$refs.sl.setOrderBaseOnAttachPrice(price)
                break
            case 2:
                this.$refs.ts.setOrderBaseOnAttachPrice(price)
                break
            case 3:
                this.$refs.l.setOrderBaseOnAttachPrice(price)
                break
            case 4:
                this.$refs.b.setOrderBaseOnAttachPrice(price)
                break
            }
        }
    },
    mounted() {
        // console.log(this)
    }
}
</script>
<style>

</style>