# from app.app import config_app
# # du fichier app.py dans le dossier app j'importe la fonction config_app
#
# if __name__ == "__main__":
#     app = config_app("production")
#     app.run(debug=True)

from app.app import app
# du fichier app.py dans le dossier app j'importe la fonction config_app

if __name__ == "__main__":
    app.run(debug=True)