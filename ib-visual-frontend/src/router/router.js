import Vue from 'vue'
import VueRouter from 'vue-router'
import BarChart from '../views/BarChart.vue'
import MainChart from '../views/MainChart.vue'

Vue.use(VueRouter)

const routes = [
    {path: '/', component: MainChart},
    {path: '/main', component: MainChart},
    {path: '/bar', component: BarChart},
]



export default new VueRouter({
    routes
})