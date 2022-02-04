
import  {createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/pages/Dashboard.vue'
import Entrance from '../components/pages/Entrance.vue'
import User from '../components/pages/user/core.vue'
import UserRegistry from '../components/pages/user/registry.vue'
import UserForm from '../components/pages/user/form.vue'
import Login from '../components/pages/Login.vue'


const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/entrance',
    name: 'Entrance',
    component: Entrance
  },
  {
    path: '/user',
    name: 'User Accounts',
    component: User,
    children: [
      {
        path: '/user',
        component: UserRegistry
      },
      {
        path: '/user/f',
        name: 'Form',
        component: UserForm
      }
    ]
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