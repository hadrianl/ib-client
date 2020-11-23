import Vue from 'vue'
import VueRouter from 'vue-router'
import MarketChart from '../views/MarketChart.vue'
import MainChart from '../views/MainChart.vue'
import ExtraChart from '../views/ExtraChart.vue'
import AnalysisChart from '../views/AnalysisChart.vue'

Vue.use(VueRouter)

const routes = [
    {path: '/', component: MainChart},
    {path: '/main', component: MainChart},
    {path: '/market', component: MarketChart},
    {name: 'extrachart', path: '/extrachart', component: ExtraChart},
    {path: '/analysis', component: AnalysisChart},
]

export default new VueRouter({
    routes
})