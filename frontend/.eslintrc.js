module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-recommended', // Per il supporto di Vue 3
    'eslint:recommended',
    'plugin:prettier/recommended', // Usa Prettier in combinazione con ESLint
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
  },
  rules: {
    // Aggiungi qui le regole specifiche per il tuo progetto
  },
}
