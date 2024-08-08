<!-- src/components/UserLogin.vue -->
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
  import axios from 'axios';
  
  export default {
    name: 'UserLogin',
    setup() {
      const form = ref({
        username: '',
        password: ''
      });
  
      const onSubmit = async () => {
        try {
            await axios.post('http://localhost:3000/api/login', form.value);
            alert('Login avvenuto con successo');
        } catch (error) {
            console.error(error);
            alert('Errore nel login');
        }
      };

  
      return { form, onSubmit };
    }
  };
  </script>
  
  <style scoped>
  /* Aggiungi stili personalizzati qui se necessario */
  </style>
  