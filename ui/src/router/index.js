import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import VoteObjectView from '../views/VoteObjectView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/votes',
    name: 'Votes',
    component: VoteObjectView
  },
]

const router = new VueRouter({
  routes
})

export default router
