from app.app import app
import os
# du fichier app.py dans le dossier app j'importe la fonction config_app

if __name__ == "__main__":
    app = app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app = app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.run(debug=True)
