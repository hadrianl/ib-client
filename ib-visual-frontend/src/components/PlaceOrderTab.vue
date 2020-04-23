<template>
    <v-card>
        <v-tabs v-model="tab">
            <v-tab :key="1">触发止损单</v-tab>
            <v-tab :key="2">均线止损单</v-tab>
            <v-tab :key="3">移动止损单</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
            <v-tab-item :key="1">
                <StopLossOrder />
            </v-tab-item>
            <v-tab-item :key="2">
                <MAStopLossOrder />
            </v-tab-item>
            <v-tab-item :key="3">
                <TrailStopOrder />
            </v-tab-item>
        </v-tabs-items>
    </v-card>
    
</template>
<script>
import StopLossOrder from './OrderTable/StopLossOrder.vue'
import MAStopLossOrder from './OrderTable/MAStopLossOrder.vue'
import TrailStopOrder from './OrderTable/TrailStopOrder.vue'
export default {
    data() {
        return {
            tab: null
            // contractsList: [],
        }
    },
    components:{
        StopLossOrder,
        MAStopLossOrder,
        TrailStopOrder,
    },
    mounted() {

    }
}
</script>
<style>
    .tabs-style > .ivu-tabs-card > .ivu-tabs-content {
        /* height: 120px; */
        margin-top: -16px;
    }

    .tabs-style > .ivu-tabs-card > .ivu-tabs-content > .ivu-tabs-tabpane {
        background: #fff;
        padding: 16px;
    }

    .tabs-style > .ivu-tabs.ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab {
        border-color: transparent;
    }

    .tabs-style > .ivu-tabs-card > .ivu-tabs-bar .ivu-tabs-tab-active {
        border-color: #fff;
    }

</style>