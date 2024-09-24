// frontend/src/axiosConfig.js
import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://13.60.212.129:5000', // Cambia con l'URL del tuo backend
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

export default instance
