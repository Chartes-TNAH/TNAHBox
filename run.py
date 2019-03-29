from app.app import app
import os
# du fichier app.py dans le dossier app j'importe la fonction config_app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
# le module os permet de communiquer avec le système d'exploitation sous-jacent (Mac, Ubuntu, etc.)
from flask_migrate import Migrate

chemin_actuel = os.path.abspath('app/')
# on stocke le chemin du fichier courant
templates = os.path.join(chemin_actuel, "templates")
# on stocke le chemin vers les templates
statics = os.path.join(chemin_actuel, "static")
# on stocke le chemin vers les statics

db = SQLAlchemy()
# on initie l'objet SQLAlchemy

login = LoginManager()
# on met en place la gestion d'utilisateur-rice-s

app = Flask(
    __name__,
    template_folder=templates,
    static_folder=statics
    )
# on initie l'app où le nom __name__ sera précisé dans la configuration (config_app())
# et on définit les dossiers contenants les templates et les statics

migrate = Migrate(app, db)

app = app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app = app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.run(debug=True)
