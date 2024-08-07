const express = require('express');
const bcrypt = require('bcryptjs');
const User = require('../models/User');

const router = express.Router();

// Registrazione
router.post('/register', async (req, res) => {
  const { username, password } = req.body;

  try {
    // Controlla se l'utente esiste già
    let user = await User.findOne({ username });
    if (user) return res.status(400).send('User already exists');

    // Crea un nuovo utente
    const hashedPassword = await bcrypt.hash(password, 10);
    user = new User({ username, password: hashedPassword });
    await user.save();

    res.status(201).send('User registered');
  } catch (error) {
    res.status(500).send('Server error');
  }
});

module.exports = router;
