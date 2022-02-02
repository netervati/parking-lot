
import  {createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/pages/Dashboard.vue'
import Login from '../components/pages/Login.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  }
]

const router = createRouter({
    mode: 'history',
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router