<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="positions"
    hide-default-footer
    class="elevation-1">
    </v-data-table>

    <!-- <Table :height="height" :columns="columns" :data="positions" :row-class-name="rowClassName">
    </Table> -->
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
                        value: 'posision'
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
        // var _this = this
        // this.$ibws.on('positions', function (ps) {
        //     console.log(ps)
        //     // _this.positionsArr = ps
        //     _this.$store.commit('initPositions', ps)
        // })
        
        // this.$ibws.on('position', function (p) {
        //     console.log(p)
        //     // for (let i in _this.positionsArr){
        //     //     if (_this.positionsArr[i].conId === p.conId){
        //     //         _this.positionsArr.splice(i, 1, p)
        //     //             return
        //     //         }
        //     //     }
    
        //     // _this.positionsArr.unshift(p)
        //     _this.$store.commit('updatePosition', p)
            
        // })

        // this.$ibws.send({'action': "get_all_positions"})
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