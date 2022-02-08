
import  {createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../components/pages/dashboard/core.vue'
import Parking from '../components/pages/parking/core.vue'
import ParkingRegistry from '../components/pages/parking/registry.vue'
import ParkingForm from '../components/pages/parking/form.vue'
import Entrance from '../components/pages/entrance/core.vue'
import EntranceRegistry from '../components/pages/entrance/registry.vue'
import EntranceForm from '../components/pages/entrance/form.vue'
import Spot from '../components/pages/spot/core.vue'
import SpotRegistry from '../components/pages/spot/registry.vue'
import SpotForm from '../components/pages/spot/form.vue'
import User from '../components/pages/user/core.vue'
import UserRegistry from '../components/pages/user/registry.vue'
import UserForm from '../components/pages/user/form.vue'
import Login from '../components/pages/login/core.vue'


const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/parking',
    name: 'Parking',
    component: Parking,
    children: [
      {
        path: '/parking',
        component: ParkingRegistry
      },
      {
        path: '/parking/f',
        component: ParkingForm
      }
    ]
  },
  {
    path: '/entrance',
    name: 'Entrance',
    component: Entrance,
    children: [
      {
        path: '/entrance',
        component: EntranceRegistry
      },
      {
        path: '/entrance/f',
        component: EntranceForm
      }
    ]
  },
  {
    path: '/spot',
    name: 'Spot',
    component: Spot,
    children: [
      {
        path: '/spot',
        component: SpotRegistry
      },
      {
        path: '/spot/f',
        component: SpotForm
      }
    ]
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