const User = require('../models/User');

// Funzione per creare un utente
exports.createUser = async (req, res) => {
  try {
    const newUser = new User({
      username: req.body.username,
      password: req.body.password,
    });
    await newUser.save();
    res.status(201).json(newUser);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};
