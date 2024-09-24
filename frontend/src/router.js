import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './views/HomePage.vue'
import UserLogin from './components/UserLogin.vue'
import UserRegister from './components/UserRegister.vue'

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: HomePage,
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin,
  },
  {
    path: '/register',
    name: 'UserRegister',
    component: UserRegister,
  },
]

const router = createRouter({
  history: createWebHistory(), // Usa createWebHistory per Vue 3
  routes,
})

export default router
