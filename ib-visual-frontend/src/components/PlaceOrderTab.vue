<template>
    <div class="tabs-style" style="background: #e3e8ee;padding:16px;">
        <Tabs type="card" value="name1">
                <TabPane label="止损单" name="name1"><StopLossOrder /></TabPane>
                <TabPane label="均线止损单" name="name2"><MAStopLossOrder /></TabPane>
            </Tabs>
    </div>  
</template>
<script>
import StopLossOrder from './OrderTable/StopLossOrder.vue'
import MAStopLossOrder from './OrderTable/MAStopLossOrder.vue'
export default {
    data() {
        return {
            // contractsList: [],
        }
    },
    components:{
        StopLossOrder,
        MAStopLossOrder,
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