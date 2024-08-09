import axios from 'axios';

// Imposta l'URL base per la tua API
axios.defaults.baseURL = 'http://<ngrok-url>'; // Sostituisci <ngrok-url> con l'URL di ngrok

// Aggiungi l'intestazione ngrok-skip-browser-warning a tutte le richieste
axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'any-value';

export default axios;
