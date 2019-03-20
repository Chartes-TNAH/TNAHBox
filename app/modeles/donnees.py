from flask import url_for
from ..app import login
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .. app import db

HasTag = db.Table('HasTag',
    db.Column('hasTag_doc_id', db.Integer, db.ForeignKey('Document.document_id'), primary_key=True),
    db.Column('hasTag_tag_id', db.Integer, db.ForeignKey('Tag.tag_id'), primary_key=True))

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

    @staticmethod
    def add_doc(title, description, format, date, matiere, downloadLink):
        """
        Fonction qui permet d'ajouter un nouveau document dans la BDD
        :param title: titre donné au document (str)
        :param description: courte présentation sur le doc (str)
        :param format: "image", "texte", "code" ou "autre" (str)
        :param date: date du cours rentrée par utilisateur (str)
        :param matiere: matière de l'enseignement (str)
        :param downloadLink: lien de téléchargement du document (str)
        :return:
        """
        erreurs = []
        if not title:
            erreurs.append("Veuillez renseigner un titre pour ce document.")
        if not description:
            erreurs.append("Veuillez renseigner une description pour ce document.")
        if not format:
            erreurs.append("Veuillez renseigner un format pour ce document.")
        if not date:
            erreurs.append("Veuillez renseigner une date pour ce document.")
        if not matiere:
            erreurs.append("Veuillez renseigner une matière pour ce document.")
        if not downloadLink:
            erreurs.append("Veuillez renseigner un lien de téléchargement pour ce document.")

        docu = Document(document_title=title,
                        document_description=description,
                        document_format=format,
                        document_date=date,
                        document_teaching=matiere,
                        document_dowloadLink=downloadLink)
        # on ajoute une nouvelle entrée dans la table document avec les champs correspondant aux paramètres du modèle

        try:
            # On essaie d'ajouter le document à la BDD
            db.session.add(docu)
            db.session.commit()

            return docu
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associate_docu_and_user(user_id, docu_id):
        '''
        Fonction qui permet d'asssocier un user à un document et
        de créer un nouvel enregistrement dans Authorship
        :param user_id: identifiant de l'auteur du document (int)
        :param docu_id: identifiant du document importé par l'utilisateur (int)
        :return: renvoie une liste d'erreurs s'il y en a
        '''
        erreurs = []
        if not user_id:
            erreurs.append("Il n'y a pas d'utilisateur à asssocier")
        if not docu_id:
            erreurs.append("Il n'y a pas de document à asssocier")

        new_association = Authorship.insert().values(authorship_person_id=user_id,
                                                     authorship_document_id=docu_id)
        # je force l'ajout d'un nouvel enregistrement
        # dans la table de relation Authorship

        db.session.execute(new_association)
        # On envoie le paquet
        db.session.commit()

        return erreurs



class Tag(db.Model):
    __tablename__ = "Tag"
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)

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
