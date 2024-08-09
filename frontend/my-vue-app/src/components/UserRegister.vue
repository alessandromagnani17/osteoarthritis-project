<template>
  <div class="register">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">AWS Project</a>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-5">
      <h2 class="mb-4">Register</h2>
      <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="form.username" id="username" type="text" class="form-control" required />
          <div class="invalid-feedback">Please enter a valid username.</div>
        </div>
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input v-model="form.name" id="name" type="text" class="form-control" required />
          <div class="invalid-feedback">Please enter your name.</div>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="form.password" id="password" type="password" class="form-control" required />
          <div class="invalid-feedback">Please enter a valid password.</div>
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from '../axiosConfig';

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
        alert('Registration successful');
        console.log('User registered:', response.data);
        form.value = { username: '', name: '', password: '' };
        router.push({ name: 'Welcome', query: { username: response.data.username } });
      } catch (error) {
        if (error.response) {
          console.error('Registration error:', error.response.data);
          alert(`Error in registration: ${error.response.data.message || error.message}`);
        } else {
          console.error('Error making request:', error.message);
          alert(`Error in registration: ${error.message}`);
        }
      }
    };

    return { form, onSubmit };
  }
};
</script>

<style scoped>
.register {
  background: #f0f8ff;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 600px;
  padding: 20px;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: auto;
  margin-bottom: auto;
}

h2 {
  font-size: 2rem;
  color: #343a40;
}

.form-label {
  color: #343a40;
}

.invalid-feedback {
  color: #dc3545;
}

.btn {
  margin-top: 10px;
  background-color: #007bff;
  border: none;
}

.btn:hover {
  background-color: #0056b3;
}
</style>
