from flask import render_template, request, flash, redirect
from flask_login import current_user, login_user, logout_user

from ..app import app
# on importe l'application provenant du fichier app.py un niveau au dessus dans l'arborescence des dossiers

from ..constantes import CONSTANTE1, CONSTANTE2
# on importe des constantes du fichier constantes.py un niveau au dessus dans l'arborescence des dossiers
from ..modeles.donnees import Document
# on importe la classe Document du fichier donnees.py contenu dans le dossier modeles

from ..modeles.utilisateurs import User
# on importe la classe User du fichier utilisateurs.py contenu dans le dossier modeles


