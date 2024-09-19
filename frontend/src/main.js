// frontend/src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from './axiosConfig'; // Importa l'istanza configurata di Axios

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import '@fortawesome/fontawesome-free/css/all.min.css';

const app = createApp(App);

// Aggiungi Axios all'istanza Vue
app.config.globalProperties.$axios = axios;

app.use(router).mount('#app');
