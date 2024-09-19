module.exports = {
    root: true,
    env: {
      node: true
    },
    extends: [
      'plugin:vue/vue3-essential',
      'eslint:recommended',
      '@vue/prettier'
    ],
    parser: '@babel/eslint-parser',
    parserOptions: {
      requireConfigFile: false,
      babelOptions: {
        presets: ['@babel/preset-env']
      },
      ecmaVersion: 2020,  // Specifica la versione ECMAScript
      sourceType: 'module' // Assicura che il parser riconosca i moduli ES6
    },
    plugins: [
      'prettier'
    ],
    rules: {
      'prettier/prettier': ['error', { singleQuote: true, semi: false }],
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }] // Aggiunge una regola per variabili non utilizzate
    }
  }
  