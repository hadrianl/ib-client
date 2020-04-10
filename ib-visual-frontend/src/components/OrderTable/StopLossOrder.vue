<template>
    <v-form>
        <v-list dense>
            <v-subheader>参考成本</v-subheader>
            <v-list-item-group>
                <v-list-item>
                    <v-btn @click="setOrderBaseOnCost(openCost)">
                        参考开仓成本：{{ openCost[1] }}@{{ parseInt(openCost[1]!=0?openCost[0]/openCost[1]:openCost[0]) }}
                    </v-btn>
                </v-list-item>
                <v-list-item>
                    <v-btn @click="setOrderBaseOnCost(sessionCost)">
                        参考会话成本：{{ sessionCost[1] }}@{{ parseInt(sessionCost[1]!=0?sessionCost[0]/sessionCost[1]:sessionCost[0]) }}
                    </v-btn>
                </v-list-item>
                <v-list-item>
                    <v-btn @click="setOrderBaseOnCost(totalCost)">
                        参考总成本  ：{{ totalCost[1] }}@{{ parseInt(totalCost[1]!=0?totalCost[0]/totalCost[1]:totalCost[0]) }}
                    </v-btn>
                </v-list-item>
                <v-list-item>
                    <v-text-field v-model="costOffset" label="costOffset" type="number" outlined></v-text-field>
                </v-list-item>      
            </v-list-item-group>        
        </v-list>
        <v-row>
            <v-text-field v-model="limitPrice" label="limitPrice" type="number" disabled outlined></v-text-field>
            <v-text-field v-model="volume" label="volume" type="number" outlined></v-text-field>
        </v-row>
        <v-row>
            <v-text-field v-model="stopPrice" label="stopPrice" type="number" outlined></v-text-field>
            <v-text-field v-model="offset" label="offset" type="number" outlined></v-text-field>
        </v-row>
        <v-text-field v-model="orderRef" label="orderRef" placeholder="Order Ref" clearable></v-text-field>
        <v-btn-toggle v-model="action" rounded>
            <v-btn value="BUY">BUY</v-btn>
            <v-btn value="SELL">SELL</v-btn>
        </v-btn-toggle>
        <v-row>
            <v-btn @click="insertOrder()">{{action?action:"NotSet"}}</v-btn>
            <v-btn @click="reset()">RESET</v-btn>
        </v-row>
    </v-form>




    <!-- <Form :label-width="60" label-position="left">
        <List border>
             
            <ListItem>
                <Button @click="setOrderBaseOnCost(openCost)">
                    参考开仓成本：{{ openCost[1] }}@{{ parseInt(openCost[1]!=0?openCost[0]/openCost[1]:openCost[0]) }}
                </Button>
            </ListItem>
            <ListItem>
                <Button @click="setOrderBaseOnCost(sessionCost)">
                    参考会话成本：{{ sessionCost[1] }}@{{ parseInt(sessionCost[1]!=0?sessionCost[0]/sessionCost[1]:sessionCost[0]) }}
                </Button>
            </ListItem>
            <ListItem>
                <Button @click="setOrderBaseOnCost(totalCost)">
                    参考总成本  ：{{ totalCost[1] }}@{{ parseInt(totalCost[1]!=0?totalCost[0]/totalCost[1]:totalCost[0]) }}
                </Button> 
            </ListItem>
            <ListItem>
                <InputNumber v-model="costOffset" :step="priceTick" ></InputNumber> 
            </ListItem>
        </List>
        <FormItem label="Price">
            <Row>
                <i-col span="14">
                    <InputNumber v-model="limitPrice" disabled :max="maxPrice" :min="minPrice" :step="priceTick" style="width: auto"></InputNumber>
                </i-col>
                <i-col span="4">@</i-col>
                <i-col span="6">
                    <InputNumber v-model="volume" :min="1" style="width: auto"></InputNumber>
                </i-col>
            </Row>
        </FormItem>
        <FormItem label="Ref">
            <Input v-model="orderRef" placeholder="order ref" clearable />
        </FormItem>
        <FormItem label="StopPrice" inline>
            <InputNumber v-model="stopPrice" :max="maxPrice" :min="minPrice" :step="priceTick"></InputNumber>
            <Icon v-if="action == 'BUY'" type="ios-arrow-round-up" color="red" />
            <Icon v-else-if="action == 'SELL'" type="ios-arrow-round-down" color="green" />
            <Icon v-else type="ios-help" />
            <InputNumber v-model="offset"   :max="200" :min="minPrice" :step="priceTick" ></InputNumber>
        </FormItem>
        <FormItem label="Action">
            <RadioGroup v-model="action" type="button" size="large">
                <Radio label="BUY" style="color:red"></Radio>
                <Radio label="SELL" style="color:green"></Radio>
            </RadioGroup>
        </FormItem>
            <Button @click="insertOrder()" size="large" :style="actionStyle">{{action?action:"NotSet"}}</Button>
            <Button @click="reset()" style="margin-left: 8px" size="large">RESET</Button>
	</Form> -->
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
                split: 0.3,
                selectedTab: 'accounts', // accounts positions orders trades
                action: "",
				volume: 1,
                priceTick: 1,
                stopPrice: 0,
                offset: 0,
				priceDecs: 0,
                maxPrice: Infinity,
                minPrice: 0,
                orderRef: "",
                costOffset: 60,
			};
        },
    mounted() {

    },
    computed: {
        limitPrice() {
            switch (this.action) {
                    case "BUY":
                        return this.stopPrice + this.offset
                    case "SELL":
                        return this.stopPrice - this.offset
                    default:
                        return 0
                }
        },
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
    methods: {
        insertOrder() {
            // const contract = this.$refs.contract.currentContract
            const contract = this.contract
            if (contract == null) {
                this.$Notice.error({
                    title: 'Order Failed!',
                    desc: "请先选择合约",
                    duration: 5
                })
                return
            }

            if (this.action == "") {
                this.$Notice.error({
                    title: 'Order Failed!',
                    desc: "请先选择方向",
                    duration: 5
                })
                return

            }

            var order = new Order()
            order.outsideRth = true
            order.orderType = 'STP LMT'
            // order.tif = 'GTC'
            order.lmtPrice = this.limitPrice
            order.auxPrice = this.stopPrice
            order.action = this.action
            order.totalQuantity = this.volume
            console.log({'action': 'place_order', 'contract': contract, 'order': order})
            this.$ibws.send({'action': 'place_order', 'contract': contract, 'order': order})


        },
        setOrderBaseOnCost(cost){
            console.log(cost)
            if(!cost[1]){
                this.$Notice.error({
                    title: 'Set Order Ref failed!',
                    desc: "无法参考0持仓设置止损单",
                    duration: 1
                })
                return
            }

            this.volume = Math.abs(cost[1])
            const avgCost = parseInt(cost[0]/cost[1])
            this.stopPrice = cost[1]>0? avgCost + this.costOffset:avgCost - this.costOffset
            this.action = cost[1]>0?"SELL":"BUY"
            this.orderRef = `sl-${this.volume}@${avgCost}`
        },
        reset() {
            // this.$refs.contract.currentContract = null
            this.volume = 1
            this.stopPrice = 0
            this.offset = 0
            this.action = ""
        },
		}
}
</script>