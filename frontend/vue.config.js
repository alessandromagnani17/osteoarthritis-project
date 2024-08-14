module.exports = {
  devServer: {
    proxy: 'https://localhost:3000',
    changeOrigin: true,
    secure: false
  }
}
