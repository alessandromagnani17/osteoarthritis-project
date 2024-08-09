<template>
    <div class="welcome">
      <div class="container mt-5 text-center">
        <h2>Welcome, {{ username }}!</h2>
        <p>You have successfully logged in to the Radiology Portal.</p>
        <router-link to="/dashboard" class="btn btn-primary btn-lg mt-4">Go to Dashboard</router-link>
        <router-link to="/" class="btn btn-secondary btn-lg mt-4">Go to Home</router-link>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    name: 'WelcomePage',
    setup() {
      const route = useRoute();
      const username = ref(route.query.username);
  
      return { username };
    }
  };
  </script>
  
  <style scoped>
  .welcome {
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
  
  p {
    font-size: 1.4rem;
    color: #6c757d;
  }
  
  .btn {
    margin-top: 12px;
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
  