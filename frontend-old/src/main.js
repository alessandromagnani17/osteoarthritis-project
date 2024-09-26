import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Amplify } from 'aws-amplify'
import awsExports from './aws-exports' // Importa la configurazione di Amplify

// Importa solo gli stili CSS che ti servono
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import '@fortawesome/fontawesome-free/css/all.min.css'

// Configura Amplify
Amplify.configure(awsExports)

const app = createApp(App)

// Usa il router, ma non AmplifyVue
app.use(router).mount('#app')
