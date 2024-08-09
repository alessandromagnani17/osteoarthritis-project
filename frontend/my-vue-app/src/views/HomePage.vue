<template>
  <div class="home">
    <div class="container text-center">
      <h1 class="display-3">Welcome to Radiology Portal</h1>
      <p class="lead">
        A comprehensive platform for viewing and managing knee radiographs, tailored for doctors and patients.
      </p>
      <img src="../assets/knee-xray.png" alt="Knee X-Ray" class="img-fluid mb-4" />
      <div class="mt-4">
        <router-link to="/register" class="btn btn-primary btn-lg mx-2">Register</router-link>
        <router-link to="/login" class="btn btn-secondary btn-lg mx-2">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};
</script>

<style scoped>
.home {
  background: #e9ecef;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  max-width: 700px;
  padding: 30px;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2.8rem;
  color: #212529;
}

p {
  font-size: 1.4rem;
  color: #6c757d;
}

.btn {
  margin: 12px;
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

.img-fluid {
  max-width: 100%;
  height: auto;
}
</style>
