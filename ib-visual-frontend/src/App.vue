<template>
  <v-app id="inspire">
    <v-navigation-drawer
    v-model="drawer"
    :expand-on-hover="true"
    dark
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
              {{ $t(`nav.${item.text}`) }}
            </v-list-item-action-text>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar
    app
    clipped-left
    color="primary">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-text-field
      v-model="hostname"
      placeholder="backend hostname"
      :disabled=noedit
      hide-details="auto"
      solo
      single-line />
      <v-btn color="success" @click.stop=connectBackend class="mx-2">{{$t('button.connect')}}</v-btn>
      <v-btn color="error" @click.stop=stopBackend class="mx-2">{{$t('button.stop')}}</v-btn>
      <v-spacer />
      <ContractItem></ContractItem>
      <v-menu offset-y>
      <template v-slot:activator="{ on }">
        <v-btn
          color="primary"
          dark
          v-on="on"
        >
          {{$i18n.locale}}
        </v-btn>
      </template>
      <v-list>
        <v-list-item
          v-for="(item, index) in langItems"
          :key="index"
          @click="$i18n.locale = item.value"
        >
          <v-list-item-title>{{ item.text }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
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
    
    <v-footer app value='fixed' padless>
      <v-col
      class='ma-0 pa-0'
      cols="12">
        <v-system-bar
        :color="isConnect?'success':'error'"
        >
          <v-spacer></v-spacer>
          <span><strong>{{isConnect?$t('connState.connected'):$t('connState.disconnected')}}</strong></span>
          <v-spacer></v-spacer>
        </v-system-bar>
      </v-col>
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
        { icon: 'mdi-handshake', text: 'trade', path: '/main' },
        { icon: 'mdi-trending-up', text: 'market' , path: '/market'}],
      langItems: [
        {text: "English", value: "en"},
        {text: "中文", value: "zh"},
      ],
			activeItem: "order",
			hostname: "localhost",
			noedit: false,
			contentHeight: document.body.clientHeight - 400
		}
  },
  mounted() {

      this.$ibws.on('error', e => {
          this.notice({
            color: 'error',
            title: 'Error',
            content: e,
          })
      }
      )

      this.$ibws.on('open', () => {
          this.notice({
            color: 'success',
            title: 'Connection',
            content: 'Connect Opened!',
          })
      })

      this.$ibws.on('close', () => {
          this.notice({
            color: 'warning',
            title: 'Connection',
            content: 'Connect Closed!',
          })
      })

      this.$ibws.on('death', () => {
          this.notice({
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
		connectBackend(){
			this.$ibws.setUrl(this.hostname)
			this.$ibws.init(false)
			this.noedit = true
    },
    stopBackend() {
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
