from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import config

db = SQLAlchemy()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.get_absolute_db_uri()
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.template_folder = config.abs_path_templates_folder()
app.static_folder = config.abs_path_static_folder()

db.init_app(app)

from my_app import routes
from my_app import data_models
