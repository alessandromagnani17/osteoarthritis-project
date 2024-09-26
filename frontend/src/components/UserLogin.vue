<template>
  <div class="login">
    <div class="container mt-5">
      <h2 class="mb-4">Login to Your Account</h2>
      <form class="needs-validation" novalidate @submit.prevent="onSubmit">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            class="form-control"
            :class="{ 'is-invalid': errors.username }"
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
            :class="{ 'is-invalid': errors.password }"
            required
          />
          <div class="invalid-feedback">{{ errors.password }}</div>
        </div>
        <div class="mb-3 form-check">
          <input
            id="rememberMe"
            v-model="form.rememberMe"
            type="checkbox"
            class="form-check-input"
          />
          <label for="rememberMe" class="form-check-label">Remember Me</label>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue' // Importa il composable ref da Vue 3
import { useRouter } from 'vue-router' // Importa il router per la navigazione
import { Auth } from '@aws-amplify/auth'

export default {
  name: 'UserLogin',
  setup() {
    // Stato del form
    const form = ref({
      username: '',
      password: '',
      rememberMe: false,
    })

    // Stato degli errori
    const errors = ref({
      username: '',
      password: '',
    })

    const router = useRouter() // Inizializza il router

    // Funzione per validare il form
    const validateForm = () => {
      errors.value = {
        username: form.value.username ? '' : 'Username is required',
        password: form.value.password ? '' : 'Password is required',
      }
      return Object.values(errors.value).every((error) => !error)
    }

    // Funzione per gestire il submit del form
    const onSubmit = async () => {
      if (!validateForm()) return

      try {
        // Effettua il login con AWS Cognito usando Auth.signIn
        const user = await Auth.signIn(form.value.username, form.value.password)
        alert('Login successful! Welcome ' + user.username)

        // Naviga alla pagina di benvenuto
        router.push({
          name: 'Welcome',
          query: { username: form.value.username },
        })
      } catch (error) {
        console.error('Login error:', error)
        alert(`Login error: ${error.message || error}`)
      }
    }

    return { form, onSubmit, errors }
  },
}
</script>

<style scoped>
.login {
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

.form-check-label {
  color: #495057;
}
</style>
