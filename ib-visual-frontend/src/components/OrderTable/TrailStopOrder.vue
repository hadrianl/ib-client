<template>
    <v-form>
        <v-list dense>
            <!-- <v-list-item>
                <v-text-field v-model="limitPrice" label="limitPrice" type="number" :rules="priceRules" disabled outlined dense></v-text-field>
                <v-text-field 
                v-model="volume"
                prepend-icon="mdi-location-enter"
                label="volume" 
                type="number"
                :rules="priceRules"
                outlined
                dense>
                </v-text-field>
            </v-list-item> -->
            <v-list-item>
                <v-text-field v-model="trailStopPrice" label="trailStopPrice" type="number" :rules="priceRules" outlined dense></v-text-field>
                <v-text-field 
                v-model="volume"
                prepend-icon="mdi-location-enter"
                label="volume" 
                type="number"
                :rules="priceRules"
                outlined
                dense>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-text-field v-model="trailAmount" label="trailAmount" type="number" :rules="priceRules" outlined dense>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-up-circle':'mdi-arrow-down-circle':''}}</v-icon>
                    </template>
                </v-text-field>
                <v-text-field 
                v-model="lmtPriceOffset" 
                label="lmtPriceOffset" 
                type="number"
                :rules="priceRules"
                outlined
                dense>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-up-circle':'mdi-arrow-down-circle':''}}</v-icon>
                    </template>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-text-field v-model="orderRef" label="orderRef" placeholder="Order Ref" clearable dense></v-text-field>
            </v-list-item>
            <v-list-item>
                <v-btn-toggle
                v-model="action" 
                rounded 
                dense
                class="mx-auto pm-auto">
                    <v-btn value="BUY" color="red">BUY</v-btn>
                    <v-btn value="SELL" color="green">SELL</v-btn>
                </v-btn-toggle>
            </v-list-item>
            <v-list-item>
                <v-row justify="space-around">
                    <v-col cols="8">
                        <v-btn 
                        block
                        @click="insertOrder()" 
                        :color="action?action=='BUY'?'red':'green':''"
                        :disabled="!action"
                        >{{action?action:"NotSet"}}</v-btn>
                    </v-col>
                    <v-col cols="4">
                        <v-btn 
                        block
                        @click="reset()" >RESET</v-btn>
                    </v-col>  
                </v-row>
            </v-list-item>
        </v-list>
    </v-form>


</template>
<script>
import {Order} from '../../plugins/datastructure.js'
// import ContractItem from '../ContractItem.vue'
// import ContractItemVue from '../ContractItem.vue'
// const patt = /^([A-Z]{3,})(\d{4})$/i
export default {
    components:{
        // ContractItem
    },
    data() {
			return {
                action: "",
				volume: "1",
                priceTick: 1,
                trailStopPrice: "0",
                trailAmount: "0",
                lmtPriceOffset: "0",
                orderRef: "",
                priceRules: [
                    // v => /^\\d+$/.test(v)
                ]
			};
        },
    mounted() {

    },
    computed: {
        limitPrice() {
            const sp = parseInt(this.stopPrice)
            const offset = parseInt(this.offset)
            switch (this.action) {
                    case "BUY":
                        return sp + offset
                    case "SELL":
                        return sp - offset
                    default:
                        return 0
                }
        },
        contract() {
            return this.$store.state.currentContract
        },
    },
    methods: {
        insertOrder() {
            // const contract = this.$refs.contract.currentContract
            const contract = this.contract
            if (contract == null) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择合约",
                    timeout: 2000
                })
                return
            }

            if (this.action == "") {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择方向",
                    timeout: 2000
                })
                return

            }

            var order = new Order()
            order.outsideRth = true
            order.orderType = 'TRAIL LIMIT'
            // order.tif = 'GTC'
            order.trailStopPrice = parseInt(this.trailStopPrice)
            order.lmtPriceOffset = parseInt(this.lmtPriceOffset)
            order.auxPrice = parseInt(this.trailAmount)
            order.action = this.action
            order.totalQuantity = parseInt(this.volume)
            order.orderRef = this.orderRef
            console.log({'action': 'place_order', 'contract': contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': contract, 'order': order})


        },
        reset() {
            this.volume = "1"
            this.trailStopPrice = "0"
            this.lmtPriceOffset = "0"
            this.trailAmount = "0"
            this.action = ""
        },
		}
}
</script>