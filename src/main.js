import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { rise } from './rise'
import './styles/base.css'

createApp(App).use(router).directive('rise', rise).mount('#app')
