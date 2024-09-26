import boto3
from flask import current_app

def get_cognito_client():
    return boto3.client(
        'cognito-idp',
        region_name=current_app.config['AWS_REGION']
    )
