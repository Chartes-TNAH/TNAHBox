from flask import url_for
import datetime

from .. app import db

# Convention : les classes portent un nom commençant par une majuscule

class Person(db.Model):
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
    person_promotion=(db.DateTime)
    person_is_admin=db.Column(db.Boolean)
    authorships = db.relationship("Authorship", back_populates="person")

class Authorship(db.Model):
    authorship_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    authorship_document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
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
    hasTag_tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))
    hasTag_doc_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
    tag = db.relationship("Tag", back_populates="hasTag")
    document = db.relationship("Document", back_populates="hasTag")

class Tag(db.Model):
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)
    hasTag=db.relationship("HasTag", back_populates="tag")
