const express = require('express');
const router = express.Router();
const UserController = require('../controllers/userController');

// Definisci le rotte
router.post('/register', UserController.createUser);

module.exports = router;
