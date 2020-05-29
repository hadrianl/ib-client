<template>
    <v-data-table
    :height="height"
    :headers="headers"
    :items="accountValues"
    fixed-header
    disable-pagination
    calculate-widths
    sort-by="tag"
    hide-default-footer
    class="elevation-1"
    >

    </v-data-table>
</template>
<script>
export default {
    data() {
        return {
            headers : [
                {
                    text: 'account', 
                    value: 'account',
                    divider: true,
                },
                {
                    text: 'tag',
                    value: 'tag',
                    align: 'center',

                },
                {
                    text: 'value',
                    value: 'value',
                    align: 'center',
                },
                {
                    text: 'currency',
                    value: 'currency',
                    divider: true,
                    align: 'center',
                },
                {
                    text: 'modelCode',
                    value: 'modelCode',
                    align: 'center',
                    sortable: false,
                },
            ]
        }
    },
    props: {
			height: {
                type: String,
                defalut: "300"
			},
        },
    created() {

    },
    computed: {
        accountValues() {
            return this.$store.state.accountValues
        }
    },
    methods: {
    }
}
</script>