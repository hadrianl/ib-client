<template>
    <v-menu
      v-model="menu"
      :close-on-content-click="false"
      :nudge-width="300"
      offset-y
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="indigo"
          dark
          v-bind="attrs"
          v-on="on"
        >
          {{$t('button.VaR')}}
        </v-btn>
      </template>

      <v-card :max-width="400">
        <v-list>
          <v-list-item>
            <v-list-item-content class="grey--text text-darken-1 mb-2">
                <v-list-item-title>VaR估计</v-list-item-title>
                {{info}}
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-divider></v-divider>

        <v-list>
            <v-list-item>
                <v-switch
                v-model="isMonteCarlo"
                label="蒙特卡罗模拟"
                ></v-switch>
            </v-list-item>
          <v-list-item>
            <v-slider
            v-model="confidence"
            label="置信区间"
            min="95"
            max="99"
            thumb-color="red"
            thumb-label="always"
            >
                <template v-slot:append>
                    <v-text-field
                        v-model="confidence"
                        class="mt-0 pt-0"
                        hide-details
                        single-line
                        type="number"
                        style="width: 60px"
                    ></v-text-field>
                </template>
            </v-slider>
          </v-list-item>

          <v-list-item>
            <v-slider
            v-model="windows"
            label="时长"
            min="60"
            max="300"
            thumb-color="red"
            thumb-label="always"
            >
                <template v-slot:append>
                    <v-text-field
                        v-model="windows"
                        class="mt-0 pt-0"
                        hide-details
                        single-line
                        type="number"
                        style="width: 60px"
                    ></v-text-field>
                </template>
            </v-slider>
          </v-list-item>
        </v-list>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn
            text
            @click="closeVaR"
          >
            Close
          </v-btn>
          <v-btn
            color="primary"
            text
            @click="calcVaR"
          >
            Calc
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
</template>
<script>
export default {
    data() {
        return {
            menu: false,
            isMonteCarlo: false,
            confidence: 95,
            windows: 60,
            info: "",
        }
    },
    props: [
        "get_datas",
    ],
    computed:{
        contract() {
            return this.$store.state.currentContract
        },
        portfolio() {
            return this.$store.getters.currentPortfolio
        }
    },
    methods: {
        calcVaR() {
            
            let pos = this.portfolio?this.portfolio.position:0
            if (!pos) {
                this.info = `没有合约持仓，在险价值为0`
                return
            }

            let {close} = this.get_datas(Infinity)
            console.log(close)
            let params = {"data": close, "confidence": this.confidence, "windows": this.windows}
            if (this.isMonteCarlo) params['method'] = 'MonteCarlo'
            this.$axios.post('../api/var', params).then(
                (res)=>{
                    console.log(res)
                    let VaR = res.data.VaR
                    this.info = `基于${close.length}个bar与合约持仓：${pos}，有${this.confidence}%的信心认为未来${this.windows}个bar的最大亏损(VaR)不超过${VaR.toFixed(2)}点`
                }
            ).catch(
                (err) => {
                    this.info = err
                }
            )
        },
        closeVaR() {
            this.menu = false
        },
    },
    watch: {
        menu(v) {
            if (!v) {
                this.info = ""
            } 
        }
    }
}
</script>