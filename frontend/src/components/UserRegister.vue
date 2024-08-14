<template>
  <div class="register">
    <div class="container mt-5">
      <h2 class="mb-4">Create Your Account</h2>
      <form @submit.prevent="onSubmit" class="needs-validation" novalidate>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input v-model="form.username" id="username" type="text" class="form-control" :class="{'is-invalid': errors.username}" required />
          <div class="invalid-feedback">{{ errors.username }}</div>
        </div>
        <div class="mb-3">
          <label for="name" class="form-label">Full Name</label>
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
        const response = await axios.post('/api/users/register', form.value);
        alert('Registration successful!');
        console.log('User registered:', response.data);
        form.value = { username: '', name: '', password: '' };
        router.push({ name: 'Welcome', query: { username: response.data.username } });
      } catch (error) {
        console.error('Registration error:', error); // Log completo dell'errore
        let errorMessage = 'An unknown error occurred.';

        if (error.response) {
          // Risposta dal server
          const { status, data } = error.response;
          console.error('Response status:', status);
          console.error('Response data:', data);

          if (data && data.message) {
            errorMessage = data.message;
          } else {
            errorMessage = `Error: ${status}`;
          }
        } else if (error.request) {
          // Richiesta effettuata ma senza risposta
          console.error('Request made but no response received:', error.request);
          errorMessage = 'No response from server.';
        } else {
          // Qualcosa è andato storto nella configurazione della richiesta
          console.error('Error setting up request:', error.message);
          errorMessage = `Request setup error: ${error.message}`;
        }

        alert(`Error in registration: ${errorMessage}`);
      }
    };

    return { form, onSubmit, errors };
  }
};
</script>


<style scoped>
.register {
  background: linear-gradient(135deg, #f7f7f7, #e0e0e0);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  max-width: 600px;
  padding: 40px;
  border-radius: 15px;
  background: #ffffff;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
  animation: slideIn 1s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateY(-30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

h2 {
  font-size: 2.5rem;
  color: #343a40;
}

.form-label {
  color: #495057;
}

.invalid-feedback {
  color: #dc3545;
}

.btn {
  margin-top: 20px;
  background-color: #007bff;
  border: none;
  transition: background-color 0.3s, transform 0.3s;
}

.btn:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}
</style>
