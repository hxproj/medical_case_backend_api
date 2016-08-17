from flask_sqlalchemy import SQLAlchemy
from flask import Flask

__version__ = '0.0.1'
__author__ = 'Craig.C.Li'
app = Flask(__name__)
app.config.from_object('config.default')
db = SQLAlchemy(app)
from src import controller
app.config['VERSION'] = __version__