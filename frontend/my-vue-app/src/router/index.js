import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue'; 
import UserRegister from '../components/UserRegister.vue';
import UserLogin from '../components/UserLogin.vue';

const routes = [
  {
    path: '/',
    name: 'HomePage', 
    component: HomePage
  },
  {
    path: '/register',
    name: 'Register',
    component: UserRegister
  },
  {
    path: '/login',
    name: 'Login',
    component: UserLogin
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
