import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AWS_REGION = os.getenv('AWS_REGION')
    COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
    COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')
