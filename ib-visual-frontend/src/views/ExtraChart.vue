<template>
    <highcharts :options="$route.params"></highcharts>
</template>
<script>
export default {
    data() {
        return {

        }
    },
    created() {
        console.log(this)
        console.log(this.$route.params)
    },
    mounted() {
        console.log(this.$route.params)
    }
}
</script>