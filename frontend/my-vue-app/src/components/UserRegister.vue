<!-- src/components/UserRegister.vue -->
<template>
  <form @submit.prevent="onSubmit">
    <label for="username">Username</label>
    <input v-model="form.username" id="username" type="text" />
    <label for="password">Password</label>
    <input v-model="form.password" id="password" type="password" />
    <button type="submit">Register</button>
  </form>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'UserRegister',
  setup() {
    const form = ref({
      username: '',
      password: ''
    });

    const onSubmit = async () => {
      try {
        await axios.post('http://localhost:3000/register', form.value);
        alert('User registered successfully');
      } catch (error) {
        console.error(error);
      }
    };

    return { form, onSubmit };
  }
};
</script>

<style scoped>
/* Aggiungi gli stili qui */
</style>
