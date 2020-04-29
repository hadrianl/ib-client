<template>
    <v-list dense>
            <v-list-group :value="false">
                <template v-slot:activator>
                    <v-list-item-content>
                        <v-list-item-title>参考成本</v-list-item-title>
                    </v-list-item-content>
                </template>
                <v-list-item-group v-model="cost">
                    <v-list-item :value="openCost" @click="costRefClick(openCost)">
                        参考开仓成本：{{ openCost[1] }}@{{ parseInt(openCost[1]!=0?openCost[0]/openCost[1]:openCost[0]) }}
                    </v-list-item>
                    <v-list-item :value="sessionCost" @click="costRefClick(sessionCost)">
                        参考会话成本：{{ sessionCost[1] }}@{{ parseInt(sessionCost[1]!=0?sessionCost[0]/sessionCost[1]:sessionCost[0]) }}
                    </v-list-item>
                    <v-list-item :value="totalCost" @click="costRefClick(totalCost)">
                        参考总成本  ：{{ totalCost[1] }}@{{ parseInt(totalCost[1]!=0?totalCost[0]/totalCost[1]:totalCost[0]) }}
                    </v-list-item>
                </v-list-item-group>    
            </v-list-group> 
        </v-list>
</template>
<script>
export default {
    data() {
        return {
            cost: null,
        }
    },
    computed: {
        contract() {
            return this.$store.state.currentContract
        },
        openCost() {
            return this.$store.getters.currentOpenCost
        },
        sessionCost() {
            return this.$store.getters.currentSessionCost
        },
        totalCost() {
            return this.$store.getters.currentTotalCost
        },
    },
    watchs: {
    },
    methods: {
        costRefClick(cost) {
            if(!cost || !cost[1]){
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Set Order Ref failed!',
                    content: "无法参考0持仓设置止损单",
                    timeout: 4000
                })
                // this.cost = null
                return
            }

            console.log(cost)

            this.$bus.$emit('costReference', cost)
        }
    },
}
</script>