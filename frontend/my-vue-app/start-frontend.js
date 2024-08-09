const { exec } = require('child_process');
const ngrok = require('@ngrok/ngrok');

// Porta del server Vue.js
const VUE_PORT = 8080;

// Token di autenticazione ngrok
const NGROK_AUTH_TOKEN = '2kNGF0kYcxhYdx1F5Hv1dy8Loh1_2Y16Ncwzw1b6N21dqBjtG'; // Sostituisci con il tuo token ngrok

// Funzione per avviare il server di sviluppo Vue.js
const startVueServer = () => {
  return new Promise((resolve, reject) => {
    console.log('Avvio del server Vue.js...');
    const vueProcess = exec('npm run serve', { cwd: __dirname });

    vueProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
      // Risolvi la promessa quando il server Vue.js è pronto
      if (data.includes('Local:')) {
        console.log('Server Vue.js avviato con successo.');
        resolve(vueProcess);
      }
    });

    vueProcess.stderr.on('data', (data) => {
      console.error(`stderr: ${data}`);
    });

    vueProcess.on('error', (error) => {
      reject(error);
    });
  });
};

// Funzione asincrona per avviare ngrok
const startNgrok = async () => {
  try {
    console.log('Avvio del server Vue.js e ngrok...');
    // Avvia il server Vue.js
    const vueProcess = await startVueServer();

    // Attendi che il server Vue.js sia completamente avviato
    console.log('Attesa di 2 secondi per l\'avvio del server Vue.js...');
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Imposta il token di autenticazione
    console.log('Impostazione del token di autenticazione ngrok...');
    await ngrok.authtoken(NGROK_AUTH_TOKEN);
    console.log('Token di autenticazione impostato.');

    // Avvia ngrok sulla porta 8080
    console.log('Avvio di ngrok sulla porta 8080...');
    const ngrokListener = await ngrok.connect({
      addr: VUE_PORT
    });

    // Stampa di debug per analizzare la struttura dell'oggetto restituito
    console.log('ngrokListener:', ngrokListener);  // Stampa l'intero oggetto
    console.log('Type of ngrokListener:', typeof ngrokListener);  // Tipo dell'oggetto

    // Assicurati di ottenere l'URL dal risultato chiamando il metodo url()
    if (ngrokListener && typeof ngrokListener === 'object' && typeof ngrokListener.url === 'function') {
      console.log('Ngrok Tunnel URL:', ngrokListener.url()); // Chiama il metodo url() per ottenere l'URL
    } else {
      console.log('Ngrok Listener non contiene il metodo url o non è un oggetto valido');
    }

    // Gestisci l'uscita
    process.on('SIGINT', () => {
      console.log('Terminazione del server Vue.js e ngrok...');
      vueProcess.kill('SIGINT'); // Termina il server Vue.js
      ngrok.disconnect(); // Chiudi ngrok
      process.exit();
    });
  } catch (err) {
    console.error('Errore nella connessione a ngrok:', err);
  }
};

// Avvia ngrok e il server Vue.js
startNgrok();
