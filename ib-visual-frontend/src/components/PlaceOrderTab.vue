<template>
    <Tabs type="card" value="name1">
        <TabPane label="止损单" name="name1"><StopLossOrder /></TabPane>
        <TabPane label="均线止损单" name="name2"></TabPane>
    </Tabs>
</template>
<script>
import StopLossOrder from './OrderTable/StopLossOrder.vue'
export default {
    data() {
        return {}
    },
    components:{
        StopLossOrder
    } 
}
</script>