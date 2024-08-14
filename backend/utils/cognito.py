import boto3
from flask import current_app

def get_cognito_client():
    return boto3.client(
        'cognito-idp',
        region_name=current_app.config['AWS_REGION']
        # Non passare aws_access_key_id e aws_secret_access_key
        # perché boto3 le recupera automaticamente dalle variabili d'ambiente
    )
