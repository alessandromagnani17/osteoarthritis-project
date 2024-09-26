from flask import Blueprint, jsonify
from flask_cors import cross_origin
from utils.cognito import get_cognito_client

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@cross_origin()
def list_users():
    client = get_cognito_client()

    try:
        response = client.list_users(UserPoolId=current_app.config['COGNITO_USER_POOL_ID'])
        return jsonify(response['Users'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
