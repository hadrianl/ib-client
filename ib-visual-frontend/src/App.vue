<template>
  <v-app id="inspire">
    <v-navigation-drawer
    v-model="drawer"
    :expand-on-hover="true"
    app
    clipped>
      <v-list dense>
        <v-list-item
        v-for="item in items"
        :key="item.text"
        :to="item.path"
        link>
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
            <v-list-item-action-text>
              {{ item.text }}
            </v-list-item-action-text>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
    app
    clipped-left
    color="blue">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-text-field
      v-model="hostname"
      placeholder="backend hostname"
      :disabled=noedit
      class="mt-8 pa-8"
      solo
      single-line />
      <v-btn color="success" @click.stop=connectBackendWS>连接</v-btn>
      <v-btn color="error" @click.stop=stopBackendWS>停止</v-btn>
      <v-spacer />
      <ContractItem class="mt-5 pa-8"></ContractItem>
    </v-app-bar>
    <v-content>
        <router-view></router-view>
    </v-content>
    <v-snackbar 
    v-model="snackbar.isShow"
    :color="snackbar.color"
    left
    bottom 
    :multi-line="true"
    :timeout="snackbar.timeout">
      {{snackbar.title}}<br/>
      {{snackbar.content}}
      <v-btn
      color="indigo"
      text
      @click="snackbar.isShow = false">Close</v-btn>
    
    </v-snackbar>
    <v-footer app>
      <v-row
      align="center"
      justify="center">
        <v-alert
        width="100%"
        dense
        text
        class="text-center"
        :type="isConnect?'success':'error'">
        {{isConnect?"已连接":"未连接"}}</v-alert>
      </v-row>
        
    </v-footer>
  </v-app>


</template>

<script>
import ContractItem from './components/ContractItem.vue'

export default {
	name: 'App',
	components: {
    ContractItem,
  },
	data() {
		return {
      snackbar: {
        isShow: false,
        color: "",
        title: "",
        content: "",
        timeout: 3000
      },
      drawer: null,
      currentPage: 0,
      items: [
        { icon: 'mdi-youtube-subscription', text: '交易', path: '/main' },
        { icon: 'mdi-trending-up', text: '行情' , path: '/bar'}],
			activeItem: "order",
			hostname: "localhost",
			noedit: false,
			contentHeight: document.body.clientHeight - 400
		}
  },
  mounted() {
      var _this = this
      this.$ibws.on('error', function(e) {
          _this.notice({
            color: 'error',
            title: 'Error',
            content: e,
          })
      }
      )

      this.$ibws.on('open', function() {
          _this.notice({
            color: 'success',
            title: 'Connection',
            content: 'Connect Opened!',
          })
      })

      this.$ibws.on('close', function() {
          _this.notice({
            color: 'warning',
            title: 'Connection',
            content: 'Connect Closed!',
          })
      })

      this.$ibws.on('death', function() {
          _this.notice({
            color: 'error',
            title: 'Connection',
            content: 'Connect Failed',
            timeout: 0
          })
      })

    // global event bus 
    this.$bus.$on('notice', this.notice)
  },
	computed: {
    isConnect() {
      return this.$store.state.isConnected
    }
		},
	methods: {
		changeContent(page) {
			this.currentPage=page
		},
		connectBackendWS(){
			this.$ibws.setUrl(this.hostname)
			this.$ibws.init(false)
			this.noedit = true
    },
    stopBackendWS() {
      if(this.$ibws.isReady()){
        this.$ibws.send({'action': 'disconnect_ib'})
      }else{
        this.$bus.$emit('notice', {
        color: 'error',
        title: 'Stop IB Failed!',
        content: "未连接，无法停止IB后台",
        timeout: 3000})
      }
      
    },
    notice(payload) {
      payload.isShow = true
      payload.timeout = 'timeout' in payload?payload.timeout:3000
      Object.assign(this.snackbar, payload)
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
