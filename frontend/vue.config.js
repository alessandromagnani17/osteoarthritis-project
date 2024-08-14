// vue.config.js
module.exports = {
  devServer: {
    port: 8080, // La stessa porta su cui gira il tuo server di sviluppo Vue.js
    host: '0.0.0.0',
    https: false,
    allowedHosts: 'all',
    client: {
      webSocketURL: {
        hostname: '0.0.0.0',
        port: 8080,
        protocol: 'ws',
      },
    },
  },
  configureWebpack: {
    stats: {
      all: false,
      errors: true,
      warnings: true
    }
  }
};
