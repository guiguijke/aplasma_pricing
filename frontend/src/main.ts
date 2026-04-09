import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import './assets/style.css'
import App from './App.vue'
import router from './router'
import { useConfigStore } from './stores/config'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(naive)

// Load config before mounting
const configStore = useConfigStore()
configStore.load().finally(() => {
  app.mount('#app')
})
