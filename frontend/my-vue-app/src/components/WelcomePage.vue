<template>
    <div class="container mt-5">
      <h2>Benvenuto, {{ username }}!</h2>
      <p>Hai effettuato l'accesso con successo.</p>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    name: 'WelcomePage',
    setup() {
      const route = useRoute();
      // Estrai il nome utente dalla query string
      const username = ref(route.query.username);
  
      return { username };
    }
  };
  </script>
  
  <style scoped>
  /* Aggiungi stili personalizzati qui se necessario */
  </style>
  