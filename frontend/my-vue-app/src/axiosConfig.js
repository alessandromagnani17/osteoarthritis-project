
        import axios from 'axios';

        axios.defaults.baseURL = 'https://3fe6-2a05-9d41-75e-0-54fb-bf5-bfe3-5da9.ngrok-free.app';
        axios.defaults.headers.common['ngrok-skip-browser-warning'] = 'any-value';
        axios.defaults.headers.common['User-Agent'] = 'custom-agent/1.0';

        // Aggiungi questo per il debug
        axios.interceptors.request.use(request => {
          console.log('Starting Request', request);
          return request;
        });

        axios.interceptors.response.use(response => {
          console.log('Response:', response);
          return response;
        });

        export default axios;
      