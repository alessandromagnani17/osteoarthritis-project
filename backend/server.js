// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const userRoutes = require('./routes/userRoutes');
const app = express();
const Users = require('./models/User');
const bcrypt = require('bcrypt');

// Porta del server Express
const EXPRESS_PORT = 3000;

// Connessione a MongoDB
var db = require('./database');
mongoose.connect(db.url);

mongoose.connection.on('connected', () => {
  console.log('Mongoose è connesso a ' + db.url);
});

// Middleware
app.use(cors()); 

app.use(express.json());

// Middleware to add ngrok-skip-browser-warning header
app.use((req, res, next) => {
  res.setHeader('ngrok-skip-browser-warning', 'true');
  next();
});

app.use('/api/users', userRoutes);

// Rotta API per login
app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await Users.findOne({ username });
    if (user && await bcrypt.compare(password, user.password)) {
      res.status(200).json({ message: 'Login successful' });
    } else {
      res.status(401).json({ message: 'Invalid credentials' });
    }
  } catch (err) {
    console.error('Errore:', err);
    res.status(500).send(err);
  }
});

// Rotta API per ottenere gli utenti
app.get('/api/users', async (req, res) => {
  try {
    const users = await Users.find();
    res.status(200).json(users);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Avvio del Server Express
app.listen(EXPRESS_PORT, '0.0.0.0', () => {
  console.log(`Server is running on port ${EXPRESS_PORT}`);
});
