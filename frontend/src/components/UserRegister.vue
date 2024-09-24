<template>
  <div class="register">
    <div class="container mt-5">
      <h2 class="mb-4">Create Your Account</h2>
      <form @submit.prevent="onSubmit">
        <div class="mb-3">
          <label for="username" class="form-label">Username (Email)</label>
          <input
            id="username"
            v-model="form.username"
            type="email"
            class="form-control"
            required
          />
          <div v-if="errors.username" class="invalid-feedback">
            {{ errors.username }}
          </div>
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
          <div v-if="errors.password" class="invalid-feedback">
            {{ errors.password }}
          </div>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          <span v-if="loading">Registering...</span>
          <span v-else>Register</span>
        </button>
        <div v-if="errors.general" class="invalid-feedback mt-3">
          {{ errors.general }}
        </div>
      </form>
      <button
        class="btn btn-secondary mt-3"
        :disabled="loading"
        @click="signInWithProvider"
      >
        <span v-if="loading">Loading...</span>
        <span v-else>Login with OAuth</span>
      </button>
    </div>
  </div>
</template>

<script>
import { Auth } from 'aws-amplify' // Assicurati di importare Auth

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      errors: {},
      loading: false, // Aggiunto per il caricamento
    }
  },
  methods: {
    async onSubmit() {
      this.loading = true // Inizia il caricamento
      try {
        const { username, password } = this.form

        // Esegui la registrazione
        await Auth.signUp({
          username,
          password,
          attributes: {
            email: username, // Passa l'email come attributo
          },
        })

        alert(
          'Registration successful! Please check your email for verification.'
        )
        this.errors = {} // Pulisce gli errori dopo il successo
      } catch (error) {
        console.error('Error signing up:', error)

        // Gestione errori Cognito
        if (error.code === 'UsernameExistsException') {
          this.errors.username = 'Username already exists.'
        } else {
          this.errors.general = error.message // Mostra l'errore generale
        }
      } finally {
        this.loading = false // Fine del caricamento
      }
    },
    async signInWithProvider() {
      this.loading = true
      try {
        await Auth.federatedSignIn() // Avvia il processo di accesso federato
      } catch (error) {
        console.error('Error during federated sign in', error)
        this.errors.general = 'Error during OAuth login.' // Errore generale
      } finally {
        this.loading = false
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
