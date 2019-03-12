from flask import url_for
import datetime

from .. app import db

# Convention : les classes portent un nom commençant par une majuscule

# On crée notre modèle de document
class Document(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    label = db.Column(db.String(120))
    format = db.Column(db.Text, nullable=False)
    date = db.DateTime()
    importDate = db.DateTime()
    downloadLink = db.Column(db.Text)
    teaching = db.Column(db.String(45), nullable=False)
