<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="positions"
    hide-default-footer
    class="elevation-1">
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

</style>