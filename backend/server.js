const express = require('express');
const mongoose = require('mongoose');
const userRoutes = require('./routes/userRoutes');
const app = express();
const Users = require('./models/User')

// Porta
const PORT = 3000; 

var db = require('./database');
mongoose.connect(db.url);

mongoose.connection.on('connected', () => {
  console.log('Mongoose è connesso a ' + db.url);
});

// Middleware
app.use(express.json());
app.use('/api/users', userRoutes);


app.post('/api/login', async (req, res) => {
  try {
    const { username, password } = req.body;
    const user = await Users.findOne({ username, password });
    if (user) {
      res.status(200).json({ message: 'Login successful' });
    } else {
      res.status(401).json({ message: 'Invalid credentials' });
    }
  } catch (err) {
    console.error('Errore:', err);
    res.status(500).send(err);
  }
});



app.get('/api/users', async (req, res) => {
  try {
    const users = await Users.find(); 
    res.status(200).json(users);
  } catch (err) {
    res.status(500).send(err);
  }
});

// Avvio del Server
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
