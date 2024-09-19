// frontend/src/router.js
import Vue from 'vue';
import Router from 'vue-router';
import HomePage from './views/HomePage.vue';
import UserLogin from './components/userLogin.vue';
import UserRegister from './components/userRegister.vue';

Vue.use(Router);

export default new Router({
  mode: 'history', // Per rimuovere il hash dalla URL
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage
    },
    {
      path: '/login',
      name: 'UserLogin',
      component: UserLogin
    },
    {
      path: '/register',
      name: 'UserRegister',
      component: UserRegister
    }
  ]
});
