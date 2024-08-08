const { exec } = require('child_process');
const ngrok = require('ngrok');

// Porta del server Vue.js
const VUE_PORT = 8080;

// Funzione per avviare il server di sviluppo Vue.js
const startVueServer = () => {
  return new Promise((resolve, reject) => {
    console.log('Avvio del server Vue.js...');
    const vueProcess = exec('npm run serve', { cwd: __dirname });

    vueProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
      // Risolvi la promessa quando il server Vue.js è pronto
      if (data.includes('Local:')) {
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
    // Avvia il server Vue.js
    const vueProcess = await startVueServer();

    // Attendi che il server Vue.js sia completamente avviato
    console.log('Attesa di 10 secondi per l\'avvio del server Vue.js...');
    await new Promise(resolve => setTimeout(resolve, 10000));

    // Avvia ngrok sulla porta 8080
    const url = await ngrok.connect(VUE_PORT);
    console.log(`Ngrok tunnel opened at: ${url}`);

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
