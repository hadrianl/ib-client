<template>
    <Tabs type="card" value="name1">
        <TabPane label="止损单" name="name1"><StopLossOrder :contractsList=contractsList /></TabPane>
        <TabPane label="均线止损单" name="name2"><MAStopLossOrder :contractsList=contractsList /></TabPane>
    </Tabs>
</template>
<script>
import StopLossOrder from './OrderTable/StopLossOrder.vue'
import MAStopLossOrder from './OrderTable/MAStopLossOrder.vue'
export default {
    data() {
        return {
            contractsList: [],
        }
    },
    components:{
        StopLossOrder,
        MAStopLossOrder,
    },
    mounted() {
        var _this = this
        this.$ibws.on('contract', function(c) {
            var flag = true
            _this.contractsList.forEach(element => {
                if (element.conId === c.conId){
                    flag = false
                }
            })
            if (flag){
                _this.contractsList.push(c)
            }
        })
    }
}
</script>