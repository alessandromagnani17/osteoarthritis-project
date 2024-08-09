<template>
    <div class="login">
      <div class="container mt-5">
        <h2 class="mb-4">Login</h2>
        <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input v-model="form.username" id="username" type="text" class="form-control" :class="{'is-invalid': errors.username}" required />
            <div class="invalid-feedback">{{ errors.username }}</div>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="form.password" id="password" type="password" class="form-control" :class="{'is-invalid': errors.password}" required />
            <div class="invalid-feedback">{{ errors.password }}</div>
          </div>
          <div class="mb-3 form-check">
            <input v-model="form.rememberMe" id="rememberMe" type="checkbox" class="form-check-input" />
            <label for="rememberMe" class="form-check-label">Remember Me</label>
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from '../axiosConfig';
  
  export default {
    name: 'UserLogin',
    setup() {
      const form = ref({
        username: '',
        password: '',
        rememberMe: false
      });
  
      const errors = ref({
        username: '',
        password: ''
      });
  
      const router = useRouter();
  
      const validateForm = () => {
        errors.value = {
          username: form.value.username ? '' : 'Username is required',
          password: form.value.password ? '' : 'Password is required'
        };
        return Object.values(errors.value).every(error => !error);
      };
  
      const onSubmit = async () => {
        if (!validateForm()) return;
  
        try {
          const response = await axios.post('http://localhost:3000/api/login', form.value, {
            headers: {
              'ngrok-skip-browser-warning': '69420'
            }
          });
          if (response.status === 200) {
            alert('Login successful');
            router.push({ name: 'Welcome', query: { username: form.value.username } });
          } else {
            alert('Invalid credentials');
          }
        } catch (error) {
          console.error('Login error:', error.response || error.message);
          alert(`Login error: ${error.response?.data.message || error.message}`);
        }
      };
  
      return { form, onSubmit, errors };
    }
  };
  </script>
  
  <style scoped>
  .login {
    background: #e9ecef;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
  
  .container {
    max-width: 700px;
    padding: 30px;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    margin: auto;
  }
  
  h2 {
    font-size: 2.2rem;
    color: #212529;
  }
  
  .form-label {
    color: #212529;
  }
  
  .invalid-feedback {
    color: #dc3545;
  }
  
  .btn {
    margin-top: 12px;
    background-color: #007bff;
    border: none;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  .form-check-label {
    color: #212529;
  }
  </style>
  