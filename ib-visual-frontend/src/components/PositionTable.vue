<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="positions"
    hide-default-footer>
    </v-data-table>

</template>
<script>
// import Vue from 'vue'
export default {
     data() {
        return {
            headers : [
                    {
                        text: 'conId',
                        value: 'conId',
                        sortable: true,
                    },
                    {
                        text: 'position',
                        value: 'position'
                    },
                    {
                        text: 'avgCost',
                        value: 'avgCost',
                    },
                    {
                        text: 'account',
                        value: 'account',
                    }]
                }
            },
     props: {
			height: {
                type: String,
                defalut: "200",
			},
        },
    computed: {
        positions() {
            return this.$store.state.positionsList
        }
    },
    created() {

    },
    mounted() {

    },
    beforeDestroy: () => {
        // 实例销毁之前调用。在这一步，实例仍然完全可用。
        // Vue.$ibws.off('positions')
        // Vue.$ibws.off('position')
    },
    methods: {
        rowClassName(row) {
            switch (true){
                case row.position > 0:
                    return 'table-positive-row'
                case row.position < 0:
                    return 'table-negative-row'
                default:
                    return 'table-normal-row'
            }
        }
    }
        }
</script>
<style>
    .ivu-table .table-positive-row td{
        background-color: #FFC1C1;
        color: #000;
    }
    .ivu-table .table-negative-row td{
        background-color: #C1FFC1;
        color: #000;
    }
    .ivu-table .table-normal-row td{
        background-color: #FFFFFF;
        color: #000;
    }
</style>