import boto3
from flask import current_app

def get_cognito_client():
    return boto3.client(
        'cognito-idp',
        region_name=current_app.config['AWS_REGION'],
        aws_access_key_id=current_app.config.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=current_app.config.get('AWS_SECRET_ACCESS_KEY')
    )
