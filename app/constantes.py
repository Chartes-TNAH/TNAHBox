from warnings import warn

# Déclaration de toutes les constantes à utiliser dans le projet
# Convention : les constantes portent des noms en majuscule

RESULTS_PER_PAGE = 9
DOSSIER_UPLOAD = "./app/static/uploads/"

SECRET_KEY = "JE SUIS UN SECRET !"
# variable nécessaire à la création d'applications Flask
# utilisée comme clé cryptographique pour générer des tokens notamment
# elle permet avec Flask-WTForm de protéger l'envoi des données
# lorsque l'utilisateur soumet des formulaires web
API_ROUTE = "/api"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)

# Les paramètres de configuration de l'application en mode test
# sont définis en tant que variables de classe au sein de la classe _TEST
class _TEST:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données de test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
# sqlite:// représente le moteur utilisé, ici SQLite
# puis / signifie ici qu'il s'agit d'un chemin relatif (un chemin absolu avec //)
# puis le chemin du fichier à aller chercher, en l'occurence db.sqlite
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class _PRODUCTION:
    SECRET_KEY = SECRET_KEY
    # On configure la base de données de production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

CONFIG = {
    "test": _TEST,
    "production": _PRODUCTION
}