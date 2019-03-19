from flask import url_for
from ..app import login
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .. app import db

HasTag = db.Table('HasTag',
    db.Column('hasTag_doc_id', db.Integer, db.ForeignKey('Document.document_id'), primary_key=True),
    db.Column('hasTag_tag_id', db.Integer, db.ForeignKey('Tag.tag_id'), primary_key=True))

# class HasTag(db.Table):
#     __tablename__ = "HasTag"
#     hasTag_doc_id = db.Column(db.Integer, db.ForeignKey('Document.document_id'), primary_key=True)
#     hasTag_tag_id = db.Column(db.Integer, db.ForeignKey('Tag.tag_id'), primary_key=True)

Authorship = db.Table('Authorship',
    db.Column('authorship_person_id', db.Integer, db.ForeignKey('Person.person_id'), primary_key=True),
    db.Column('authorship_document_id', db.Integer, db.ForeignKey('Document.document_id'), primary_key=True),
    db.Column('authorship_date', db.Text))

class Document(db.Model):
    __tablename__ = "Document"
    document_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    document_title = db.Column(db.Text)
    document_description = db.Column(db.Text)
    document_format = db.Column(db.String)
    document_date = db.Column(db.Text)
    document_teaching = db.Column(db.String)
    document_downloadLink = db.Column(db.Text)
    document_tag = db.relationship("Tag",
                    secondary=HasTag,
                    backref=db.backref("Document"))


class Tag(db.Model):
    __tablename__ = "Tag"
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)

    # def __init__(self, label):
    #     self.tag_label = label

    @staticmethod
    def add_tag(label, docu_id):
        '''
        Fonction qui permet d'ajouter un tag à un document
        :param label: label du tag à ajoute (str)
        :param docu_id: identifiant du document auquel ajouter le tag (int)
        :return: renvoie le tag nouvellement créé dans la BDD
        '''
        erreurs = []
        if not label:
            erreurs.append("Le tag fourni est vide")
        if not docu_id:
            erreurs.append("Il n'y a pas d'identifiant de document")

        tag = Tag(tag_label=label)
        # on ajoute un nouvel enregistrement à la Table Tag
        # où le champ tag_label est rempli avec la valeur de label

        new_association = HasTag.insert().values(hasTag_tag_id=tag.tag_id,
                                                 hasTag_doc_id=docu_id)

    # on fait une nouvelle entrée dans la table Authorship
    # pour associer l'id de ce nouvel enregistrement de la table Tag
    # à l'id du Document renseigné en paramètre

        try:
            # On essaie d'ajouter et de commit ces deux nouveaux enregistrements
            db.session.add(tag)
            db.session.execute(new_association)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, tag
        except Exception as erreur:
            return False, [str(erreur)]


class Person(UserMixin, db.Model):
    __tablename__ = "Person"
    person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    person_name = db.Column(db.String(25))
    person_firstName = db.Column(db.String(25))
    person_is_teacher = db.Column(db.Boolean)
    person_email = db.Column(db.Text, nullable=False)
    person_login = db.Column(db.Text,unique=True, nullable=False)
    person_password = db.Column(db.Text, unique=True, nullable=False)
    person_linkedIn = db.Column(db.Text,unique=True)
    person_cv = db.Column(db.Text)
    person_git = db.Column(db.Text, unique=True)
    person_promotion = db.Column(db.Text)
    person_is_admin = db.Column(db.Boolean)
    created_document = db.relationship("Document",
                    secondary=Authorship,
                    backref=db.backref("Person"))

    def __repr__(self):
        return '<User {}>'.format(self.person_login)

    def set_password(self, password):
        self.person_password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.person_password, password)

    def get_id(self):
        return(self.person_id)

@login.user_loader
def load_user(id):
    return Person.query.get(int(id))
