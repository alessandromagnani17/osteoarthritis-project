const { exec } = require('child_process');
const ngrok = require('@ngrok/ngrok');
const fs = require('fs');
const path = require('path');

const VUE_PORT = 8080;
const NGROK_AUTH_TOKEN = '2kNGF0kYcxhYdx1F5Hv1dy8Loh1_2Y16Ncwzw1b6N21dqBjtG';

const startVueServer = () => {
  return new Promise((resolve, reject) => {
    console.log('Avvio del server Vue.js...');
    const vueProcess = exec('npm run serve', { cwd: __dirname });

    vueProcess.stdout.on('data', (data) => {
      console.log(`stdout: ${data}`);
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

const startNgrok = async () => {
    try {
      console.log('Avvio del server Vue.js e ngrok...');
      const vueProcess = await startVueServer();
  
      console.log('Attesa di 2 secondi per l\'avvio del server Vue.js...');
      await new Promise(resolve => setTimeout(resolve, 2000));
  
      console.log('Impostazione del token di autenticazione ngrok...');
      await ngrok.authtoken(NGROK_AUTH_TOKEN);
      console.log('Token di autenticazione impostato.');
  
      console.log('Avvio di ngrok sulla porta 8080...');
      const ngrokUrl = await ngrok.connect({
        addr: VUE_PORT,
        onStatusChange: status => console.log(status),
        onLogEvent: log => console.log(log),
        host_header: 'rewrite'  // Qui viene impostato l'host_header per bypassare la pagina intermedia
      });
  
      console.log('Ngrok Tunnel URL:', ngrokUrl);
  
      const configPath = path.join(__dirname, 'src', 'axiosConfig.js');
      const configContent = `
        import axios from 'axios';
  
        axios.defaults.baseURL = '${ngrokUrl}';
        axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'any-value';
  
        export default axios;
      `;
      fs.writeFileSync(configPath, configContent, 'utf-8');
      console.log(`File di configurazione Axios aggiornato con URL Ngrok: ${ngrokUrl}`);
  
      vueProcess.stdout.pipe(process.stdout);
      vueProcess.stderr.pipe(process.stderr);
  
      process.on('SIGINT', () => {
        console.log('Terminazione del server Vue.js e ngrok...');
        vueProcess.kill('SIGINT');
        ngrok.disconnect();
        process.exit();
      });
    } catch (err) {
      console.error('Errore nella connessione a ngrok:', err);
    }
  };
  

startNgrok();
