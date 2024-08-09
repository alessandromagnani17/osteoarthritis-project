<template>
    <div class="welcome">
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">AWS Project</a>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item">
                <router-link to="/" class="nav-link">Home</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link">Register</router-link>
              </li>
              <li class="nav-item">
                <router-link to="/login" class="nav-link">Login</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div class="container mt-5 text-center">
        <h2>Welcome, {{ username }}!</h2>
        <p>You have successfully logged in.</p>
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
  
  p {
    font-size: 1.2rem;
    color: #6c757d;
  }
  
  .btn {
    margin-top: 10px;
    background-color: #6c757d;
    border: none;
  }
  
  .btn:hover {
    background-color: #5a6268;
  }
  </style>
  