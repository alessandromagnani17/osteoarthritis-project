<template>
  <div class="welcome">
    <div class="container mt-5 text-center">
      <h2>Welcome, {{ username }}!</h2>
      <p>You have successfully logged in to the Radiology Portal.</p>
      <div class="btn-group mt-4">
        <router-link to="/dashboard" class="btn btn-primary btn-lg"
          >Go to Dashboard</router-link
        >
        <router-link to="/" class="btn btn-secondary btn-lg"
          >Go to Home</router-link
        >
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'WelcomePage',
  setup() {
    const route = useRoute()
    const username = ref(route.query.username)

    return { username }
  },
}
</script>

<style scoped>
.welcome {
  background: linear-gradient(135deg, #f7f7f7, #e0e0e0);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  max-width: 700px;
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

p {
  font-size: 1.4rem;
  color: #6c757d;
}

.btn-group .btn {
  margin: 10px;
  transition: background-color 0.3s, transform 0.3s;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
  transform: scale(1.1);
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
  transform: scale(1.1);
}
</style>
