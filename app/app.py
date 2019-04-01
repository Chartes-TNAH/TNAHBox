from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
# le module os permet de communiquer avec le système d'exploitation sous-jacent (Mac, Ubuntu, etc.)
from .constantes import CONFIG
from flask_migrate import Migrate

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# on stocke le chemin du fichier courant
templates = os.path.join(chemin_actuel, "templates")
# on stocke le chemin vers les templates
statics = os.path.join(chemin_actuel, "static")
# on stocke le chemin vers les statics
uploads = os.path.join(chemin_actuel, "uploads")
# on stocke le chemin vers le dossier où stocker les fichiers uploadés

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

from .routes import routes

def config_app(config_name="test"):
    """ Create the application """
    app.config.from_object(CONFIG[config_name])
    # on configure l'app en appelant la constante CONFIG
    # qui définit s'il s'agit de l'app test ou app de production
    # la variable config_name a pour valeur de base "test"
    # les configurations sont contenues dans le fichier constantes.py
    # où les BDD associées sont définies

    # Set up extensions
    db.init_app(app)
    login.init_app(app)

    return app

app = config_app("production")
