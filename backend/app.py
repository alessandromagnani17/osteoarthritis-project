from flask import Flask

from dotenv import load_dotenv
import os
from routes.auth import auth_bp

load_dotenv()  # Carica variabili d'ambiente dal file .env

app = Flask(__name__)
app.config['AWS_REGION'] = os.getenv('AWS_REGION')
app.config['COGNITO_USER_POOL_ID'] = os.getenv('COGNITO_USER_POOL_ID')
app.config['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
app.config['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')

# Registra i blueprint
app.register_blueprint(auth_bp, url_prefix='/api')

@app.route('/')
def home():
    return "Welcome to the API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))