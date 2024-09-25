<template>
  <div class="home">
    <div class="container text-center">
      <h1 class="display-3">Welcome to Radiology Portal</h1>
      <p class="lead">
        Explore and manage radiographs with ease and efficiency, crafted for
        both doctors and patients.
      </p>
      <img
        src="../assets/knee-xray.png"
        alt="Knee X-Ray"
        class="img-fluid mb-4"
      />
      <div class="btn-group mt-4">
        <router-link to="/register" class="btn btn-primary btn-lg mx-2">
          Register
        </router-link>
        <router-link to="/login" class="btn btn-secondary btn-lg mx-2">
          Login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  mounted() {
    console.log('AWS Amplify Cognito is configured. No API calls are made.')
  },
}
</script>

<style scoped>
/* Stili rimasti invariati */
.home {
  background: linear-gradient(135deg, #ffffff, #e9ecef);
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  position: relative;
}

.container {
  max-width: 700px;
  padding: 40px;
  border-radius: 15px;
  background: #ffffff;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 3rem;
  color: #212529;
  animation: fadeIn 1.5s ease-out;
}

p {
  font-size: 1.5rem;
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

.img-fluid {
  max-width: 100%;
  height: auto;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
