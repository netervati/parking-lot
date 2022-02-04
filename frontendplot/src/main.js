import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router/index'
import 'bootstrap'

const MAIN_APP = createApp(App)

axios.defaults.baseURL = process.env.VUE_APP_API_URL
MAIN_APP.config.globalProperties.$http = axios
router.beforeEach((to, from, next) => {
    document.title = to.matched[0].name
    next()
})

MAIN_APP.use(router)
MAIN_APP.mount('#app')
