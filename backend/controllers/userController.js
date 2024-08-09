// controllers/userController.js
const bcrypt = require('bcrypt');
const User = require('../models/User');

// Funzione per creare un utente
exports.createUser = async (req, res) => {
  try {
    const { username, name, password } = req.body;

    // Verifica se l'utente esiste già
    const existingUser = await User.findOne({ username });
    if (existingUser) {
      return res.status(400).json({ message: 'Username already taken' });
    }

    // Hash della password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Crea un nuovo utente con la password hashata
    const newUser = new User({ username, name, password: hashedPassword });
    await newUser.save();

    // Rispondi con il nuovo utente creato
    res.status(201).json(newUser);
  } catch (err) {
    console.error('Error registering user:', err);
    res.status(500).json({ error: err.message });
  }
};
