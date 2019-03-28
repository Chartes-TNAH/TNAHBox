from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
# le module os permet de communiquer avec le système d'exploitation sous-jacent (Mac, Ubuntu, etc.)
from .constantes import CONFIG

# Database initialization
if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
