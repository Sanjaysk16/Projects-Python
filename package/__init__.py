from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = os.urandom(12)
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)  
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from package import routes, model

with app.app_context():
    db.create_all()