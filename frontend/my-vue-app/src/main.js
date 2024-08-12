import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './axiosConfig'; // Importa la configurazione Axios senza importare direttamente `axios`

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

// Importa Font Awesome
import '@fortawesome/fontawesome-free/css/all.min.css';

createApp(App)
  .use(router)
  .mount('#app');
