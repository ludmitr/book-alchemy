from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db.init_app(app)

from my_app import routes
from my_app import data_models
