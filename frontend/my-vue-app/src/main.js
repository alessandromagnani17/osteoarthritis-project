import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './axiosConfig'; // Importa la configurazione Axios senza importare direttamente `axios`

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

createApp(App)
  .use(router)
  .mount('#app');
