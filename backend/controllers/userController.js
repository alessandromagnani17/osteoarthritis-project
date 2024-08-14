// backend/controllers/userController.js
const AmazonCognitoIdentity = require('amazon-cognito-identity-js');
const userPool = require('../cognito');

exports.createUser = async (req, res) => {
  const { username, name, password } = req.body;

  const attributeList = [];
  attributeList.push(new AmazonCognitoIdentity.CognitoUserAttribute({
    Name: 'name',
    Value: name
  }));

  userPool.signUp(username, password, attributeList, null, (err, result) => {
    if (err) {
      console.error('Error registering user:', err);
      return res.status(500).json({ error: err.message });
    }

    const cognitoUser = result.user;
    res.status(201).json({ message: 'User registered successfully', username: cognitoUser.getUsername() });
  });
};
