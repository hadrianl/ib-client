<template>
    <div :id="id" style="height:600px"></div>
</template>
<script>
import Highcharts from 'highcharts'
import HighchartsMore from 'highcharts/highcharts-more'

HighchartsMore(Highcharts)

export default {
    data() {
        return {
            chart: null,
        }
    },
    mounted() {
        // this.chart = Highcharts.chart(this.id, this.options)
        console.group('------mounted创建时状态------');
        console.log("%c%s", "color:red" , "el     : " + this.$el); 
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message) 
    },
    props: [
        'id',
    ],
    methods: {
        updateCharts(options) {
            this.chart = Highcharts.chart(this.id, options)
        }
    },
    beforeCreate: function() {
        console.group('------beforeCreate创建前状态------');
        console.log("%c%s", "color:red" , "el     : " + this.$el); 
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message) 
    },
    created: function() {
        console.group('------created创建完毕状态------');
        console.log("%c%s", "color:red","el     : " + this.$el); 
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message); 
    },
    beforeMount: function() {
        console.group('------beforeMount挂载前状态------');
        console.log("%c%s", "color:red","el     : " + (this.$el)); 
        console.log(this.$el);
        console.log("%c%s", "color:red","data   : " + this.$data);
        console.log("%c%s", "color:red","message: " + this.message);
    },
    beforeUpdate: function () {
        console.group('beforeUpdate 更新前状态===============》');
        console.log("%c%s", "color:red","el     : " + this.$el);
        console.log(this.$el);   
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message); 
    },
    updated: function () {
        console.group('updated 更新完成状态===============》');
        console.log("%c%s", "color:red","el     : " + this.$el);
        console.log(this.$el); 
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message); 
    },
    beforeDestroy: function () {
        console.group('beforeDestroy 销毁前状态===============》');
        console.log("%c%s", "color:red","el     : " + this.$el);
        console.log(this.$el);    
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message); 
    },
    destroyed: function () {
        console.group('destroyed 销毁完成状态===============》');
        console.log("%c%s", "color:red","el     : " + this.$el);
        console.log(this.$el);  
        console.log("%c%s", "color:red","data   : " + this.$data); 
        console.log("%c%s", "color:red","message: " + this.message)
    }

}
</script>