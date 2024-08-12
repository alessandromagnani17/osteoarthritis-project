const { exec } = require('child_process');
const ngrok = require('@ngrok/ngrok');
const fs = require('fs');
const path = require('path');

const VUE_PORT = 8080;
const NGROK_AUTH_TOKEN = '2kNGF0kYcxhYdx1F5Hv1dy8Loh1_2Y16Ncwzw1b6N21dqBjtG';

const startVueServer = () => {
  return new Promise((resolve, reject) => {
    console.log('DEBUG: Avvio del server Vue.js...');
    const vueProcess = exec('npm run serve', { cwd: __dirname });

    vueProcess.stdout.on('data', (data) => {
      console.log(`DEBUG: stdout: ${data}`);
      if (data.includes('Local:')) {
        resolve(vueProcess);
      }
    });

    vueProcess.stderr.on('data', (data) => {
      console.error(`DEBUG: stderr: ${data}`);
    });

    vueProcess.on('error', (error) => {
      console.error(`DEBUG: errore: ${error}`);
      reject(error);
    });
  });
};

const startNgrok = async () => {
  try {
    console.log('DEBUG: Avvio del server Vue.js e ngrok...');
    const vueProcess = await startVueServer();
    console.log('DEBUG: Attesa di 2 secondi per l\'avvio del server Vue.js...');
    await new Promise(resolve => setTimeout(resolve, 2000));

    console.log('DEBUG: Impostazione del token di autenticazione ngrok...');
    await ngrok.authtoken(NGROK_AUTH_TOKEN);
    console.log('DEBUG: Token di autenticazione impostato.');

    console.log('DEBUG: Avvio di ngrok sulla porta 8080...');
    const ngrokSession = await ngrok.connect({
      addr: VUE_PORT,
      onStatusChange: status => console.log(`DEBUG: ngrok status: ${status}`),
      onLogEvent: log => console.log(`DEBUG: ngrok log: ${log}`)
    });

    // Aggiungiamo un controllo per ispezionare l'oggetto restituito
    console.log('DEBUG: Oggetto ngrok restituito:', ngrokSession);

    // Estrai l'URL usando la funzione 'url'
    const publicUrl = typeof ngrokSession === 'object' && ngrokSession.url ? ngrokSession.url() : null;

    if (publicUrl) {
      console.log('DEBUG: Ngrok Tunnel URL:', publicUrl);

      const configPath = path.join(__dirname, 'src', 'axiosConfig.js');

      // Leggi il contenuto attuale di axiosConfig.js
      let existingConfig = '';
      if (fs.existsSync(configPath)) {
        existingConfig = fs.readFileSync(configPath, 'utf-8');
      }

      // Modifica il contenuto
      const newConfigContent = `
        import axios from 'axios';

        axios.defaults.baseURL = '${publicUrl}';
        axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'any-value';
        axios.defaults.headers.common['User-Agent'] = 'custom-agent/1.0';

        // Aggiungi questo per il debug
        axios.interceptors.request.use(request => {
          console.log('Starting Request', request);
          return request;
        });

        axios.interceptors.response.use(response => {
          console.log('Response:', response);
          return response;
        });

        export default axios;
      `;

      // Scrivi il contenuto modificato nel file
      fs.writeFileSync(configPath, newConfigContent, 'utf-8');
      console.log(`DEBUG: File di configurazione Axios aggiornato con URL Ngrok: ${publicUrl}`);
    } else {
      console.error('DEBUG: Errore: Ngrok non ha restituito un URL valido:', publicUrl);
    }

    vueProcess.stdout.pipe(process.stdout);
    vueProcess.stderr.pipe(process.stderr);

    process.on('SIGINT', () => {
      console.log('DEBUG: Terminazione del server Vue.js e ngrok...');
      vueProcess.kill('SIGINT');
      ngrok.disconnect();
      process.exit();
    });
  } catch (err) {
    console.error('DEBUG: Errore nella connessione a ngrok:', err);
  }
};

startNgrok();
