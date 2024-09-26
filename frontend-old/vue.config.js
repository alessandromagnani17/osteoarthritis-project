module.exports = {
  devServer: {
    host: '0.0.0.0', // Ascolta su tutti gli indirizzi
    port: 8080, // Porta del frontend
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Backend Flask API
        changeOrigin: true,
        secure: false,
      },
    },
  },
}
