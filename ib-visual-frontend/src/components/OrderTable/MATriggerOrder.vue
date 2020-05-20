<template>
    <v-form v-model="valid">
        <v-list dense>
            <v-list-item>
                <v-text-field 
                v-model.number="volume" 
                label="volume" 
                type="number" 
                dense
                outlined></v-text-field>
                <v-text-field 
                v-model.number="lmtOffset" 
                label="lmtOffset" 
                type="number"
                :rules="offsetRules"
                dense
                outlined>
                    <template v-slot:prepend>
                        <v-icon
                        :color="action?action=='BUY'?'red':'green':''"
                        >{{action?action=='BUY'?'mdi-arrow-up-circle':'mdi-arrow-down-circle':''}}</v-icon>
                    </template>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-text-field 
                v-model="trigger" 
                label="triggerType" 
                placeholder="触发类型" 
                :rules="triggerRules"
                dense
                outlined></v-text-field>
                <v-text-field 
                v-model.number="triggerOffset" 
                label="triggerOffset" 
                type="number" 
                :rules="offsetRules"
                dense
                outlined>
                </v-text-field>
            </v-list-item>
            <v-list-item>
                <v-btn-toggle 
                v-model="action" 
                rounded 
                class="mx-auto pm-auto">
                    <v-btn value="BUY" color="red">BUY</v-btn>
                    <v-btn value="SELL" color="green">SELL</v-btn>
                </v-btn-toggle>
            </v-list-item>
            <v-list-item>
                <v-row justify="space-around">
                    <v-col cols="7">
                        <v-btn 
                        block
                        @click="insertOrder()" 
                        :color="action?action=='BUY'?'red':'green':''"
                        :disabled="!action">{{action?action:"NotSet"}}</v-btn>
                    </v-col>
                    <v-col cols="4">
                        <v-btn 
                        block
                        min-width="10px"
                        @click="reset()" >RESET</v-btn>
                    </v-col>  
                </v-row>
            </v-list-item>
        </v-list>
    </v-form>
</template>
<script>
import {Order} from '../../plugins/datastructure.js'
import axios from '../../plugins/axios.js'

export default {
    components:{
        // ContractItem
    },
    data() {
        return {
            action: undefined,
            volume: 1,
            lmtOffset: 0,
            triggerOffset: 0,
            trigger: '',
            triggerRules: [
                v => /^(ma)(\d+)(@(1 min|\d+ mins))?$/i.test(v)
            ],
            offsetRules: [
            ],
            valid: false,
        }
    },
    mounted() {
        axios.get('/config/default.json').then((response) => {Object.assign(this.$data, response.data['MATriggerOrder'])})
    },
    computed: {
        actionStyle() {
            switch (this.action) {
            case "BUY":
                return {
                    background: 'red'
                }
            case "SELL":
                return {
                    background: 'green'
                }
            default:
                return {
                    background: 'white'
                }
        }
        },
        contract() {
            return this.$store.state.currentContract
        }
    },
    methods: {
        insertOrder() {
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

            if (!this.action) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请先选择方向",
                    timeout: 2000
                })
                return
            }

            if (!this.valid) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请正确填写下单参数",
                    timeout: 2000
                })
                return
            }

            const options = this.getTriggerOptions()

            if (!options) {
                this.$bus.$emit('notice', {
                    color: 'error',
                    title: 'Order Failed!',
                    content: "请填写正确触发类型",
                    timeout: 2000
                })
                return
            }

            
            var order = new Order()
            // order.orderType = 'STP LMT'
            order.outsideRth = true
            order.tif = 'GTC'
            order.action = this.action
            order.totalQuantity = parseInt(this.volume)
            console.log({'action': 'place_dynamic_order', 'contract': contract, 'order': order, 'options': {}})
            this.$ibws.send({'action': 'place_dynamic_order', 'contract': contract, 'order': order, 'options': options})

        },
        reset() {
            this.volume = 1
            this.triggerOffset = 0
            this.lmtOffset = 0
            this.action = undefined
            axios.get('/config/default.json').then((response) => {Object.assign(this.$data, response.data['MATriggerOrder'])})
        },
        getTriggerOptions() {
            const ma_trigger_patt = /^(ma)(\d+)(@(1 min|\d+ mins))?$/i
            let trigger = this.trigger
            let ret = ma_trigger_patt.exec(trigger)
            let options = {}
            if (ret) {
                console.log(ret)
                const trigger_type = ret[1].toUpperCase()
                switch (trigger_type) {
                    case 'MA': {
                        let period = Number(ret[2])
                        let barSize = ret[4]
                        if (0 < period <= 120) {
                            options['type'] = trigger_type
                            options['period'] = period
                            options['barSize'] = barSize
                            options['lmtOffset'] = parseInt(this.lmtOffset)
                            options['triggerOffset'] = parseInt(this.triggerOffset)
                        }
                        break
                    }
                }
            }
            return options
        }
		}
}
</script>