import { createRouter, createWebHistory } from 'vue-router'
import NewQuote from '../views/NewQuote.vue'
import QuoteResult from '../views/QuoteResult.vue'
import History from '../views/History.vue'
import Settings from '../views/Settings.vue'
import Materials from '../views/Materials.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/new' },
    { path: '/new', component: NewQuote, name: 'new' },
    { path: '/result', component: QuoteResult, name: 'result' },
    { path: '/history', component: History, name: 'history' },
    { path: '/settings', component: Settings, name: 'settings' },
    { path: '/materials', component: Materials, name: 'materials' },
  ],
})

export default router
