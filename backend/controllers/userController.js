// controllers/userController.js
const User = require('../models/User');

// Funzione per creare un utente
exports.createUser = async (req, res) => {
  try {
    // Log dei dati in arrivo
    console.log('Request body:', req.body);

    // Estrai i dati dal corpo della richiesta
    const { username, name, password } = req.body;

    // Verifica se l'utente esiste già
    const existingUser = await User.findOne({ username });
    if (existingUser) {
      return res.status(400).json({ message: 'Username already taken' });
    }

    // Crea un nuovo utente
    const newUser = new User({ username, name, password });
    await newUser.save();

    // Rispondi con il nuovo utente creato
    res.status(201).json(newUser);
  } catch (err) {
    console.error('Error registering user:', err);
    res.status(500).json({ error: err.message });
  }
};
