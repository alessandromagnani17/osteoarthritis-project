// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Amplify } from 'aws-amplify' // Importa Amplify

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import '@fortawesome/fontawesome-free/css/all.min.css'
import awsExports from './aws-exports' // Assicurati di avere il file aws-exports.js

Amplify.configure(awsExports)

const app = createApp(App)

app.use(router).mount('#app')
