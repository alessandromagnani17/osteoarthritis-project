require('dotenv').config(); // Carica le variabili di ambiente

const express = require('express');
const cors = require('cors');
const https = require('https');
const fs = require('fs');
const { CognitoIdentityProviderClient, ListUsersCommand } = require('@aws-sdk/client-cognito-identity-provider');

// Crea un'istanza del client Cognito
const client = new CognitoIdentityProviderClient({
  region: process.env.AWS_REGION // Assicurati che questa variabile sia impostata
});

const app = express();
const EXPRESS_PORT = 3000;

// Leggi i certificati SSL
const privateKey = fs.readFileSync('server.key', 'utf8');
const certificate = fs.readFileSync('server.cert', 'utf8');
const credentials = { key: privateKey, cert: certificate };

// Middleware globale per aggiungere l'header ngrok-skip-browser-warning
app.use((req, res, next) => {
  res.setHeader('ngrok-skip-browser-warning', 'true');
  next();
});

// Middleware CORS
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'ngrok-skip-browser-warning']
}));

app.use(express.json()); // Per il parsing del corpo delle richieste JSON

// Rotta per la visualizzazione degli utenti registrati
app.get('/api/users', async (req, res) => {
  const params = {
    UserPoolId: process.env.COGNITO_USER_POOL_ID  // Assicurati che questa variabile sia impostata
  };

  const command = new ListUsersCommand(params);

  try {
    const response = await client.send(command);
    res.status(200).json(response.Users);
  } catch (err) {
    console.error('Error fetching users:', err);
    res.status(500).json({ message: 'Error fetching users', error: err.message });
  }
});

// Avvio del Server HTTPS
https.createServer(credentials, app).listen(EXPRESS_PORT, () => {
  console.log(`HTTPS Server is running on port ${EXPRESS_PORT}`);
});
