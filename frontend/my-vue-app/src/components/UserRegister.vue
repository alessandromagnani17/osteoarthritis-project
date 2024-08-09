<template>
  <div class="register">
    <div class="container mt-5">
      <h2 class="mb-4">Register</h2>
      <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="form.username" id="username" type="text" class="form-control" :class="{'is-invalid': errors.username}" required />
          <div class="invalid-feedback">{{ errors.username }}</div>
        </div>
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input v-model="form.name" id="name" type="text" class="form-control" :class="{'is-invalid': errors.name}" required />
          <div class="invalid-feedback">{{ errors.name }}</div>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input v-model="form.password" id="password" type="password" class="form-control" :class="{'is-invalid': errors.password}" required />
          <div class="invalid-feedback">{{ errors.password }}</div>
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

    const errors = ref({
      username: '',
      name: '',
      password: ''
    });

    const router = useRouter();

    const validateForm = () => {
      errors.value = {
        username: form.value.username ? '' : 'Username is required',
        name: form.value.name ? '' : 'Name is required',
        password: form.value.password ? '' : 'Password is required'
      };
      return Object.values(errors.value).every(error => !error);
    };

    const onSubmit = async () => {
      if (!validateForm()) return;

      try {
        const response = await axios.post('http://localhost:3000/api/users/register', form.value, {
          headers: {
            'ngrok-skip-browser-warning': '69420'
          }
        });
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

    return { form, onSubmit, errors };
  }
};
</script>

<style scoped>
.register {
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
</style>
