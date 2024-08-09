<template>
    <div class="container mt-5">
      <h2 class="mb-4">Login</h2>
      <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="form.username" id="username" type="text" class="form-control" required />
          <div class="invalid-feedback">Inserisci un username valido.</div>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="form.password" id="password" type="password" class="form-control" required />
          <div class="invalid-feedback">Inserisci una password valida.</div>
        </div>
        <button type="submit" class="btn btn-primary">Accedi</button>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  export default {
    name: 'UserLogin',
    setup() {
      const form = ref({
        username: '',
        password: ''
      });
  
      const router = useRouter();
  
      const onSubmit = async () => {
        try {
          const response = await axios.post('http://localhost:3000/api/login', form.value);
          if (response.status === 200) {
            alert('Login avvenuto con successo');
            // Reindirizza alla pagina di benvenuto con il nome utente
            router.push({ name: 'Welcome', query: { username: form.value.username } });
          } else {
            alert('Credenziali non valide');
          }
        } catch (error) {
          console.error('Errore nel login:', error.response || error.message);
          alert(`Errore nel login: ${error.response?.data.message || error.message}`);
        }
      };
  
      return { form, onSubmit };
    }
  };
  </script>
  
  <style scoped>
  /* Aggiungi stili personalizzati qui se necessario */
  </style>
  