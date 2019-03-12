from flask import url_for
import datetime

from .. app import db

# Convention : les classes portent un nom commençant par une majusculegit

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
    authorship = db.relationship("Authorship", back_populates="person")


class Authorship(db.Model):
    authorship_person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    authorship_document_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))
    # authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    person = db.relationship("Person", back_populates="Document_document.id")
    document = db.relationship("Document", back_populates="Person_person.id")

    # def author_to_json(self):
    #     return {
    #         "author": self.user.to_jsonapi_dict(),
    #         "on": self.authorship_date
    #     }


# On crée notre modèle de document
class Document(db.Model):
    document_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    document_title = db.Column(db.Text)
    document_description = db.Column(db.Text)
    document_format = db.Column(db.String)
    document_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    document_downloadLink = db.Column(db.Text)
    document_teaching = db.Column(db.String)
    document_importDate = db.Column(db.DateTime)
    authorship = db.relationship("Authorship", back_populates="document")
    hasTag=db.relationship("hasTag", back_populates="document")

class HasTag(db.Model):
    hasTag_tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))
    hasTag_doc_id = db.Column(db.Integer, db.ForeignKey('document.document_id'))

class Tag(db.Model):
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)

    # def to_jsonapi_dict(self):
    #     """ It ressembles a little JSON API format but it is not completely compatible

    #     :return:
    #     """
    #     return {
    #         "type": "document",
    #         "id": self.document_id,
    #         "attributes": {
    #             "name": self.document_nom,
    #             "description": self.document_description,
    #             "longitude": self.document_longitude,
    #             "latitude": self.document_latitude,
    #             "category": self.document_type
    #         },
    #         "links": {
    #             "self": url_for("lieu", document_id=self.document_id, _external=True),
    #             "json": url_for("api_documents_single", document_id=self.document_id, _external=True)
    #         },
    #         "relationships": {
    #              "editions": [
    #                  author.author_to_json()
    #                  for author in self.authorships
    #              ]
    #         }
    #     }
