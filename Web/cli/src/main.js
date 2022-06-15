import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Element from 'element-plus'
import 'element-plus/lib/theme-chalk/index.css'
import Axios from 'axios'
import * as echarts from 'echarts'
Axios.defaults.baseURL='http://localhost:5000/'
const app=createApp(App)
app.config.globalProperties.$axios = Axios
app.config.globalProperties.$echarts = echarts
app.config.productionTiAp = false
Axios.defaults.withCredentials = true
app.use(store).use(router).use(Element).mount('#app')
            