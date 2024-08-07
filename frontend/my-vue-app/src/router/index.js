// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import UserRegister from '../components/UserRegister.vue';

const routes = [
  { path: '/register', component: UserRegister },
  { path: '/', redirect: '/register' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
