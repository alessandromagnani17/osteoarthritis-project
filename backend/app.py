from flask import Flask
from routes.auth import auth_bp
from routes.users import users_bp
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(ssl_context=('server.crt', 'server.key'))
