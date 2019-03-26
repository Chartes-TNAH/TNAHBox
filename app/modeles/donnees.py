from flask import url_for
from ..app import login
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from sqlalchemy import update

from .. app import db

HasTag = db.Table('HasTag',
    db.Column('hasTag_doc_id', db.Integer, db.ForeignKey('Document.document_id'), primary_key=True),
    db.Column('hasTag_tag_id', db.Integer, db.ForeignKey('Tag.tag_id'), primary_key=True))

IsFav = db.Table('IsFav',
    db.Column('faved_docu_id', db.Integer, db.ForeignKey('Document.document_id'), primary_key=True),
    db.Column('loving_user_id', db.Integer, db.ForeignKey('Person.person_id'), primary_key=True))

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
                    backref=db.backref("Document", lazy='dynamic'))
    loving_users = db.relationship("Person",
                    secondary=IsFav,
                    backref=db.backref("Document"))

    def get_id(self):
        return(self.document_id)


    @staticmethod
    def add_doc(title, description, format, date, matiere, downloadlink):
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
        if not downloadlink:
             erreurs.append("Aucun lien de téléchargement pour ce document.")

        docu = Document(document_title=title,
                        document_description=description,
                        document_format=format,
                        document_date=date,
                        document_teaching=matiere,
                        document_downloadLink=downloadlink)
        # on ajoute une nouvelle entrée dans la table document avec les champs correspondant aux paramètres du modèle

        try:
            # On essaie d'ajouter le document à la BDD
            db.session.add(docu)
            db.session.commit()

            return docu
        except Exception as erreur:
            return False, [str(erreur)]


    @staticmethod
    def associate_docu_and_user(user, docu):
        '''
        Fonction qui permet d'asssocier un user à un document et
        de créer un nouvel enregistrement dans Authorship
        :param user: auteur du document (entrée de la BDD)
        :param docu: document importé par l'utilisateur (entrée de la BDD)
        :return: renvoie une liste d'erreurs s'il y en a
        '''
        erreurs = []
        if not user:
            erreurs.append("Il n'y a pas d'utilisateur à associer")
        if not docu:
            erreurs.append("Il n'y a pas de document à associer")

        if user is None or docu is None:
            return

        if docu not in user.created_document:
            # si le document n'est pas dans la liste de document créés par cet utilisateur
            user.created_document.append(docu)

        db.session.add(user)
        db.session.commit()

    @staticmethod
    def add_cv(user, docu):
        '''
        Fonction qui ajoute le lien d'un document sur le serveur à l'attribut "person_cv" d'un utilisateur
        :param user: utilisateur auquel ajouter le lien du document en tant que CV (entrée de la BDD)
        :param docu: document à associer (entrée de la BDD)
        :return: liste d'erreurs d'il y en a
        '''
        erreurs = []
        if not user:
            erreurs.append("Il n'y a pas d'utilisateur à associer")
        if not docu:
            erreurs.append("Il n'y a pas de document à associer")

        if user is None or docu is None:
            # si les paramètres renseignés ne correspondent à rien, je ne fais rien
            return

        user.person_cv = docu.document_downloadLink
        db.session.commit()

        return erreurs


class Tag(db.Model):
    __tablename__ = "Tag"
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '{}'.format(self.tag_label)

    def get_id(self):
        return(self.tag_id)

    @staticmethod
    def add_tag(label):
        '''
        Fonction qui permet d'ajouter un tag dans la BDD
        :param label: label du tag à ajoute (str)
        :return: renvoie le tag nouvellement créé dans la BDD
        '''
        erreurs = []
        if not label:
            erreurs.append("Le tag fourni est vide")

        all_tag_labels = Tag.query.with_entities(Tag.tag_label)
        all_tag_labels = [tlbl[0] for tlbl in all_tag_labels.all()]
        # je récupère tous les enregistrements de tag_label dans la table Tag

        if label:
            if label not in all_tag_labels:
                tag = Tag(tag_label=label)
                # si mon tag n'est pas déjà dans la table tag
                # je crée un nouvel enregistrement
                # On essaie d'ajouter et de commit ce nouvel enregistrement
                db.session.add(tag)
                db.session.commit()
            else: # si j'ai déjà un tag déjà ainsi nommé
                tag = Tag.query.filter(Tag.tag_label == label).first()
                # j'assigne à tag, la valeur de l'enregistrement dont le label
                # correspond bien à celui renseigné en paramètre

        try:
            return tag
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def associate_tag_and_docu(tag_id, docu_id):
        '''
        Fonction qui permet d'associer un tag à un document
        :param tag_id: identifiant du tag à ajouter au document (int)
        :param docu_id: identifiant du document auquel ajouter le tag (int)
        :return: renvoie une liste d'erreurs s'il y en a
        '''
        erreurs = []
        if not tag_id:
            erreurs.append("Il n'y a pas de tag à associer")
        if not docu_id:
            erreurs.append("Il n'y a pas de document à associer")

        tag = Tag.query.filter(Tag.tag_id == tag_id).first()
        # je récupère le tag correspondant à l'id
        doc = Document.query.filter(Document.document_id == docu_id).first()
        # idem pour le document

        if tag is None or doc is None:
            # si les identifiants ne correspondent à rien, je ne fais rien
            return

        if tag not in doc.document_tag:
            # si le tag n'est pas déjà dans la liste de tag contenu dans document_tag
            doc.document_tag.append(tag)
            # je l'ajoute à cette liste

        db.session.add(doc)
        db.session.commit()

        return erreurs


class Person(UserMixin, db.Model):
    __tablename__ = "Person"
    person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    person_name = db.Column(db.String(25))
    person_firstName = db.Column(db.String(25))
    person_is_teacher = db.Column(db.Boolean)
    person_email = db.Column(db.Text, nullable=False)
    person_login = db.Column(db.Text,unique=True, nullable=False)
    person_password = db.Column(db.Text, unique=True, nullable=False)
    person_linkedIn = db.Column(db.Text, unique=True)
    person_cv = db.Column(db.Text)
    person_git = db.Column(db.Text, unique=True)
    person_promotion = db.Column(db.Text)
    person_is_admin = db.Column(db.Boolean)
    person_last_seen = db.Column(db.Text, default=date)
    person_description = db.Column(db.Text)
    created_document = db.relationship("Document",
                    secondary=Authorship,
                    backref=db.backref("Person")) #, lazy='dynamic'))

    @staticmethod
    def add_docu_to_favorites(user, docu):
        '''
        Fonction qui permet d'ajouter aux favoris de l'utilisateur
        le document courant
        :param user: auteur du document (entrée de la BDD)
        :param docu: document importé par l'utilisateur (entrée de la BDD)
        :return: liste d'erreurs d'il y en a
        '''
        erreurs = []
        if not user:
            erreurs.append("Il n'y a pas d'utilisateur à associer")
        if not docu:
            erreurs.append("Il n'y a pas de document à associer")

        if user is None or docu is None:
            # si les paramètres renseignés ne correspondent à rien, je ne fais rien
            return

        if user not in docu.loving_users:
            # si le document n'est pas déjà dans la liste des documents favoris de l'utilisateur
            docu.loving_users.append(user)
            # je l'ajoute à cette liste

        db.session.add(docu)
        db.session.commit()

        return erreurs

    def remove_docu_to_favorites(user, docu):
        '''
        Fonction qui permet d'enlever aux favoris de l'utilisateur
        le document courant
        :param user: auteur du document (entrée de la BDD)
        :param docu: document importé par l'utilisateur (entrée de la BDD)
        :return: liste d'erreurs d'il y en a
        '''
        erreurs = []
        if not user:
            erreurs.append("Il n'y a pas d'utilisateur à dissocier")
        if not docu:
            erreurs.append("Il n'y a pas de document à dissocier")

        if user is None or docu is None:
            # si les paramètres renseignés ne correspondent à rien, je ne fais rien
            return

        if user in docu.loving_users:
            # si le document est déjà dans la liste des documents favoris de l'utilisateur
            docu.loving_users.remove(user)
            # je le supprime de cette liste

        db.session.add(docu)
        db.session.commit()

        return erreurs

    def __repr__(self):
        return '<User {}>'.format(self.person_login)

    def to_dict(self):
        return {
            'name': self.person_name,
            'firstName': self.person_firstName,
            'email': self.person_email,
            'git': self.person_git,
            'promotion': self.person_promotion,
        }
    # définition d'une fonction pour déterminer les éléments à afficher dans la page person comme un dictionnaire

    def set_password(self, password):
        self.person_password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.person_password, password)

    def get_id(self):
        return(self.person_id)

@login.user_loader
def load_user(id):
    return Person.query.get(int(id))
