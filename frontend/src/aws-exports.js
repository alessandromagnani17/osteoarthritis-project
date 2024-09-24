import { Amplify } from 'aws-amplify'

Amplify.configure({
  Auth: {
    Cognito: {
      // ID del tuo user pool Cognito
      userPoolId: 'eu-north-1_schiIOXTg',

      // ID del client associato al tuo user pool Cognito
      userPoolClientId: '52t5qhmjvib5ea6sqj68qup5pl',

      // Aggiungi il tuo Cognito Identity Pool ID se usi federated identities
      identityPoolId: 'eu-north-1:6f12bc1a-4f09-4a79-9fd9-169583e79097', // Sostituisci con il tuo ID, se necessario

      // Configura la modalità di login
      loginWith: {
        email: true,
      },

      // Metodo di verifica alla registrazione (code o link)
      signUpVerificationMethod: 'code',

      // Attributi obbligatori per gli utenti
      userAttributes: {
        email: {
          required: true,
        },
      },

      // Consenti l'accesso agli utenti ospiti (senza autenticazione)
      allowGuestAccess: true,

      // Regole di formato per la password
      passwordFormat: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireNumbers: true,
        requireSpecialCharacters: true,
      },
    },
  },
})

export default Amplify
