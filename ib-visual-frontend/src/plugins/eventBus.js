import Vue from 'vue'

Vue.$bus = Vue.prototype.$bus = Vue.$bus || new Vue()