import axios from 'axios'
import Vue from 'vue'

Vue.prototype.$axios = axios

var DEFAULT_CONFIG = require('@/assets/config/default.json')

// axios.get('/assets/config/default.json')
// .then((response) => console.log(response))
// .error((error) => console.log(error))

export {DEFAULT_CONFIG}