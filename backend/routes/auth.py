from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from utils.cognito import get_cognito_client

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    client = get_cognito_client()

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=current_app.config['COGNITO_APP_CLIENT_ID'],
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return jsonify({'token': response['AuthenticationResult']['AccessToken']})
    except client.exceptions.NotAuthorizedException:
        return jsonify({'error': 'Invalid credentials'}), 401
