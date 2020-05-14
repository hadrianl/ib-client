import axios from 'axios'
import Vue from 'vue'

Vue.prototype.$axios = axios

var get_default_config = axios.get('/config/default.json')


export {get_default_config}