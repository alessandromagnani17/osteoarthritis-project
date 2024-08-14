// backend/cognito.js
const { CognitoIdentityProviderClient } = require('@aws-sdk/client-cognito-identity-provider');
const dotenv = require('dotenv');

// Carica le variabili d'ambiente dal file .env
dotenv.config();

// Configura il client Cognito
const client = new CognitoIdentityProviderClient({
  region: process.env.AWS_REGION
});

module.exports = client;
