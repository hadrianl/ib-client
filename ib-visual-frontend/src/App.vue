<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
      clipped
    >
      <v-list dense>
        <v-list-item
          v-for="item in items"
          :key="item.text"
          link
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-subheader class="mt-4 grey--text text--darken-1">------------</v-subheader>
        <!-- <v-list>
          <v-list-item
            v-for="item in items2"
            :key="item.text"
            link
          >
            <v-list-item-avatar>
              <img
                :src="`https://randomuser.me/api/portraits/men/${item.picture}.jpg`"
                alt=""
              >
            </v-list-item-avatar>
            <v-list-item-title v-text="item.text" />
          </v-list-item>
        </v-list> -->
        <!-- <v-list-item
          class="mt-4"
          link
        >
          <v-list-item-action>
            <v-icon color="grey darken-1">mdi-plus-circle-outline</v-icon>
          </v-list-item-action>
          <v-list-item-title class="grey--text text--darken-1">Browse Channels</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-action>
            <v-icon color="grey darken-1">mdi-settings</v-icon>
          </v-list-item-action>
          <v-list-item-title class="grey--text text--darken-1">Manage Subscriptions</v-list-item-title>
        </v-list-item> -->
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      clipped-left
      color="red"
      dense
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
	  <v-text-field
	  	v-model="hostname"
	  	placeholder="backend hostname"
		:disabled=noedit
		single-line
	  />
	  <v-btn color="primary" @click.stop=updateBackendWS>连接</v-btn>
      <!-- <v-icon
        class="mx-4"
        large
      >
        mdi-youtube
      </v-icon> -->
      <!-- <v-toolbar-title class="mr-12 align-center">
        <span class="title">Youtube</span>
      </v-toolbar-title> -->
      <v-spacer />
      <v-row
        align="center"
        style="max-width: 650px"
      >
        <v-text-field
          :append-icon-cb="() => {}"
          placeholder="输入contract..."
          single-line
          append-icon="mdi-magnify"
          color="white"
          hide-details
        />
      </v-row>
    </v-app-bar>

    <v-content>
      <v-container class="fill-height">
        <!-- <v-row
          justify="center"
          align="center"
        >
          <v-col class="shrink">
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-btn
                  :href="source"
                  icon
                  large
                  target="_blank"
                  v-on="on"
                >
                  <v-icon large>mdi-code-tags</v-icon>
                </v-btn>
              </template>
              <span>Source</span>
            </v-tooltip>
            <v-tooltip right>
              <template v-slot:activator="{ on }">
                <v-btn
                  icon
                  large
                  href="https://codepen.io/johnjleider/pen/aezMOO"
                  target="_blank"
                  v-on="on"
                >
                  <v-icon large>mdi-codepen</v-icon>
                </v-btn>
              </template>
              <span>Codepen</span>
            </v-tooltip>
          </v-col>
        </v-row> -->
      </v-container>
    </v-content>
  </v-app>





<!-- <div class="layout">
        <Layout>
            <Header :style="{position: 'fixed', width: '100%'}">
                <Menu mode="horizontal" theme="dark" :active-name="activeItem" @on-select="selectItem">
                    <div class="layout-logo"></div>
                    <div class="layout-nav">
                        <MenuItem name="order">
                            <Icon type="ios-navigate"></Icon>
                            下单
                        </MenuItem>
                        <MenuItem name="kline">
                            <Icon type="ios-keypad"></Icon>
                            行情
                        </MenuItem>
                        <div>
                            <Icon type="ios-analytics"></Icon>
                            <Input v-model="hostname" placeholder="Enter hostname...default: localhost" size="small" style="width: 200px" :disabled="noedit"/>
							<Button type="success" ghost @click=connectBackendWS>连接</Button>
                        </div>
                    </div>
                </Menu>
            </Header>
            <Content :style="{margin: '88px 20px 0', background: '#fff', minHeight: '600px'}">
				<div v-if="activeItem=='order'">
					<MainChart />
				</div>
                <div v-else-if="activeItem=='kline'">
					<BarChart />
				</div>
            </Content>
            <Footer class="layout-footer-center">
				<Alert v-if="$store.state.isConnected" type="success" style="text-align: center">已连接</Alert>
				<Alert v-else type="error" style="text-align: center">未连接</Alert>
				<span>2020 &copy; KRData</span>
			</Footer>
        </Layout>

  </div> -->
</template>

<script>
import MainChart from './views/MainChart.vue'
import BarChart from './components/BarChart.vue'

export default {
	name: 'App',
	components: {
		MainChart,
		BarChart,
	},
	data() {
		return {
			activeItem: "order",
			hostname: "localhost",
			noedit: false,
			contentHeight: document.body.clientHeight - 400
		}
	},
	computed: {

		},
	methods: {
		selectItem(name) {
			this.activeItem=name
		},
		connectBackendWS(){
			this.$ibws.setUrl(this.hostname)
			this.$ibws.init(false)
			this.noedit = true

		}
	},
	beforeCreate: () => {
		// 在实例初始化之后，数据观测 (data observer) 和 event/watcher 事件配置之前被调用。
	},
	created: () => {
		// 在实例创建完成后被立即调用。在这一步，实例已完成以下的配置：数据观测 (data observer)，属性和方法的运算，watch/event 事件回调。然而，挂载阶段还没开始，$el 属性目前不可见。
	},
	beforeMount: () => {
		// 在挂载开始之前被调用：相关的 render 函数首次被调用。
	},
	mounted: () => {

	},
	beforeUpdate: () => {
		// 数据更新时调用，发生在虚拟 DOM 打补丁之前。这里适合在更新之前访问现有的 DOM，比如手动移除已添加的事件监听器。
	},
	updated: () => {
		// 由于数据更改导致的虚拟 DOM 重新渲染和打补丁，在这之后会调用该钩子。
		// 当这个钩子被调用时，组件 DOM 已经更新，所以你现在可以执行依赖于 DOM 的操作。然而在大多数情况下，你应该避免在此期间更改状态。如果要相应状态改变，通常最好使用计算属性或 watcher 取而代之。
		// 注意 updated 不会承诺所有的子组件也都一起被重绘。
	},
	activated: () => {
		// keep-alive 组件激活时调用。
	},
	deactivated: () => {
		// keep-alive 组件停用时调用。
	},
	beforeDestroy: () => {
		// 实例销毁之前调用。在这一步，实例仍然完全可用。
	},
	destroyed: () => {
		// Vue 实例销毁后调用。调用后，Vue 实例指示的所有东西都会解绑定，所有的事件监听器会被移除，所有的子实例也会被销毁。
	},
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
