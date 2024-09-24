<template>
  <div class="register">
    <div class="container mt-5">
      <h2 class="mb-4">Create Your Account</h2>
      <form @submit.prevent="onSubmit">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-control"
            required
          />
          <div class="invalid-feedback">{{ errors.username }}</div>
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="form-control"
            required
          />
          <div class="invalid-feedback">{{ errors.password }}</div>
        </div>
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      errors: {},
    }
  },
  methods: {
    async onSubmit() {
      try {
        const response = await axios.post('/api/login', this.form)
        alert(`Login successful! Welcome, ${response.data.username}`) // Esempio di utilizzo
      } catch (error) {
        if (error.response) {
          this.errors = error.response.data.errors || {}
          alert(`Error: ${error.response.data.error}`)
        } else {
          alert('Network error')
        }
      }
    },
  },
}
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
