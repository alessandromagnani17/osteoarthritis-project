<!-- src/views/HomePage.vue -->
<template>
  <div class="home">
    <div class="container text-center">
      <h1 class="display-3">Benvenuto nella Mia Applicazione</h1>
      <p class="lead">Un'applicazione MEVN con una semplice interfaccia per la registrazione e il login.</p>
      <div class="mt-4">
        <router-link to="/register" class="btn btn-primary btn-lg mx-2">Registrati</router-link>
        <router-link to="/login" class="btn btn-secondary btn-lg mx-2">Accedi</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
};
</script>

<style scoped>
.home {
  background: #f8f9fa;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  max-width: 600px;
  padding: 20px;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.5rem;
  color: #343a40;
}

p {
  font-size: 1.2rem;
  color: #6c757d;
}

.btn {
  margin: 10px;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-secondary:hover {
  background-color: #5a6268;
}
</style>
