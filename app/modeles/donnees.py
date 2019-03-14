from flask import url_for
from ..app import login
from flask_login import UserMixin
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from .. app import db

# Convention : les classes portent un nom commençant par une majuscule

class Person(UserMixin, db.Model):
    person_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    person_name = db.Column(db.String(25))
    person_firstName = db.Column(db.String(25))
    person_is_teacher = db.Column(db.Boolean)
    person_email = db.Column(db.Text, nullable=False)
    person_login = db.Column(db.Text,unique=True, nullable=False)
    person_password=db.Column(db.Text, unique=True, nullable=False)
    person_linkedIn=db.Column(db.Text,unique=True)
    person_cv=db.Column(db.Text)
    person_git=db.Column(db.Text, unique=True)
    person_promotion=(db.Text)
    person_is_admin=db.Column(db.Boolean)
    authorships = db.relationship("Authorship", back_populates="person")

    def __repr__(self):
        return '<User {}>'.format(self.person_login)

    def set_password(self, password):
        self.person_password= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.person_password, password)

class Authorship(db.Model):
    authorship_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'), primary_key=True)
    authorship_document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'), primary_key=True)
    authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    person = db.relationship("Person", back_populates="authorships")
    document = db.relationship("Document", back_populates="authorships")

class Document(db.Model):
    document_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    document_title = db.Column(db.Text)
    document_description = db.Column(db.Text)
    document_format = db.Column(db.String)
    document_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    document_teaching = db.Column(db.String)
    document_downloadLink = db.Column(db.Text)
    authorships = db.relationship("Authorship", back_populates="document")
    hasTag=db.relationship("HasTag", back_populates="document")

class HasTag(db.Model):
    hasTag_tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'), primary_key=True)
    hasTag_doc_id = db.Column(db.Integer, db.ForeignKey('document.document_id'), primary_key=True)
    tag = db.relationship("Tag", back_populates="hasTag")
    document = db.relationship("Document", back_populates="hasTag")

class Tag(db.Model):
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)
    hasTag=db.relationship("HasTag", back_populates="tag")

@login.user_loader
def load_user(id):
    return Person.query.get(int(Person.person_id))
