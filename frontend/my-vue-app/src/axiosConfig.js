import axios from 'axios';

axios.defaults.baseURL = 'https://7284-2a05-9d41-75e-0-54fb-bf5-bfe3-5da9.ngrok-free.app';
axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'any-value';
axios.defaults.headers.common['User-Agent'] = 'custom-agent/1.0';

// Interceptor per le richieste
axios.interceptors.request.use(request => {
  console.log('Starting Request', request);
  return request;
}, error => {
  console.error('Request Error', error);
  return Promise.reject(error);
});

// Interceptor per le risposte
axios.interceptors.response.use(response => {
  console.log('Response:', response);
  return response;
}, error => {
  console.error('Response Error', error);
  return Promise.reject(error);
});

export default axios;
