<template>
    <div class="login">
      <div class="container mt-5">
        <h2 class="mb-4">Login</h2>
        <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input v-model="form.username" id="username" type="text" class="form-control" required />
            <div class="invalid-feedback">Please enter a valid username.</div>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input v-model="form.password" id="password" type="password" class="form-control" required />
            <div class="invalid-feedback">Please enter a valid password.</div>
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
        password: ''
      });
  
      const router = useRouter();
  
      const onSubmit = async () => {
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
  
      return { form, onSubmit };
    }
  };
  </script>
  
  <style scoped>
  .login {
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
  