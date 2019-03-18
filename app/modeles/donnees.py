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
