from app.app import config_app
# du fichier app.py dans le dossier app j'importe la fonction config_app

if __name__ == "__main__":
    app = config_app()
    app.run(debug=True)