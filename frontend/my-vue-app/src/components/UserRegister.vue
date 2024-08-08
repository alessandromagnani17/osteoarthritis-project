<!-- src/components/UserRegister.vue -->
<template>
  <div class="container mt-5">
    <h2 class="mb-4">Registrati</h2>
    <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="form.username" id="username" type="text" class="form-control" required />
        <div class="invalid-feedback">Inserisci un username valido.</div>
      </div>
      <div class="mb-3">
        <label for="name" class="form-label">Nome</label>
        <input v-model="form.name" id="name" type="text" class="form-control" required />
        <div class="invalid-feedback">Inserisci il tuo nome.</div>
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="form.password" id="password" type="password" class="form-control" required />
        <div class="invalid-feedback">Inserisci una password valida.</div>
      </div>
      <button type="submit" class="btn btn-primary">Registrati</button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'UserRegister',
  setup() {
    const form = ref({
      username: '',
      name: '',
      password: ''
    });

    const onSubmit = async () => {
      try {
        await axios.post('http://localhost:3000/users', form.value);
        alert('Registrazione avvenuta con successo');
        form.value = { username: '', name: '', password: '' }; // Resetta il form
      } catch (error) {
        console.error(error);
        alert('Errore nella registrazione');
      }
    };

    return { form, onSubmit };
  }
};
</script>

<style scoped>
/* Aggiungi stili personalizzati qui se necessario */
</style>
