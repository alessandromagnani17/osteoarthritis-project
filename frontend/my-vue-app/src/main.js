// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css'; // Importa lo stile di Bootstrap

createApp(App)
  .use(router)
  .mount('#app');
