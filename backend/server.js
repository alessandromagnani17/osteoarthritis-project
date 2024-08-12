const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const https = require('https');
const fs = require('fs');
const userRoutes = require('./routes/userRoutes');
const app = express();
const Users = require('./models/User');
const bcrypt = require('bcrypt');

// Porta del server Express
const EXPRESS_PORT = 3000;

// Leggi i certificati SSL
const privateKey = fs.readFileSync('server.key', 'utf8');
const certificate = fs.readFileSync('server.cert', 'utf8');
const credentials = { key: privateKey, cert: certificate };

// Middleware globale per aggiungere l'header ngrok-skip-browser-warning
app.use((req, res, next) => {
  res.setHeader('ngrok-skip-browser-warning', 'true');
  next();
});

// Connessione a MongoDB
var db = require('./database');
mongoose.connect(db.url);

mongoose.connection.on('connected', () => {
  console.log('Mongoose è connesso a ' + db.url);
});

// Middleware CORS
app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'ngrok-skip-browser-warning']
}));

app.use(express.json());

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

// Avvio del Server HTTPS
https.createServer(credentials, app).listen(EXPRESS_PORT, () => {
  console.log(`HTTPS Server is running on port ${EXPRESS_PORT}`);
});
