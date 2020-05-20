import Vue from 'vue'
import VueRouter from 'vue-router'
import MarketChart from '../views/MarketChart.vue'
import MainChart from '../views/MainChart.vue'

Vue.use(VueRouter)

const routes = [
    {path: '/', component: MainChart},
    {path: '/main', component: MainChart},
    {path: '/market', component: MarketChart},
]



export default new VueRouter({
    routes
})