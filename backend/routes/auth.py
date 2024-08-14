from flask import Blueprint, jsonify, current_app
import boto3

auth_bp = Blueprint('auth', __name__)

def get_cognito_client():
    return boto3.client('cognito-idp', region_name=current_app.config['AWS_REGION'])

@auth_bp.route('/users', methods=['GET'])
def get_users():
    client = get_cognito_client()
    user_pool_id = current_app.config['COGNITO_USER_POOL_ID']
    
    try:
        response = client.list_users(UserPoolId=user_pool_id)
        return jsonify(response['Users'])
    except Exception as e:
        return jsonify({'message': 'Error fetching users', 'error': str(e)}), 500
