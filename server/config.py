from flask_login import LoginManager
from flask_restful import Api
from flask import Flask

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'fbi-very-secret-string'
api = Api(app)