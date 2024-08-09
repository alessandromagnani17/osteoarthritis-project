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
import { useRouter } from 'vue-router';
import axios from '../axiosConfig'; // Importa la configurazione Axios


export default {
  name: 'UserRegister',
  setup() {
    const form = ref({
      username: '',
      name: '',
      password: ''
    });

    const router = useRouter();

    const onSubmit = async () => {
      try {
        const response = await axios.post('http://localhost:3000/api/users/register', form.value);
        alert('Registrazione avvenuta con successo');
        console.log('User registered:', response.data);
        form.value = { username: '', name: '', password: '' }; // Resetta il form
        // Reindirizza alla pagina di benvenuto con il nome utente
        router.push({ name: 'Welcome', query: { username: form.value.username } });
      } catch (error) {
        if (error.response) {
          // La richiesta è stata fatta e il server ha risposto con uno stato di errore
          console.error('Registration error:', error.response.data);
          alert(`Errore nella registrazione: ${error.response.data.message || error.message}`);
        } else {
          // Qualcosa è andato storto nel fare la richiesta
          console.error('Error making request:', error.message);
          alert(`Errore nella registrazione: ${error.message}`);
        }
      }
    };

    return { form, onSubmit };
  }
};
</script>

<style scoped>
/* Aggiungi stili personalizzati qui se necessario */
</style>
