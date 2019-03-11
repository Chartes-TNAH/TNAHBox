from flask import url_for
import datetime

from .. app import db

# Convention : les classes portent un nom commençant par une majusculegit

class Authorship(db.Model):
    __tablename__ = "authorship"
     authorship_id = db.Column(db.Integer, nullable=True, autoincrement=True, primary_key=True)
    # authorship_place_id = db.Column(db.Integer, db.ForeignKey('place.place_id'))
    # authorship_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    # authorship_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # user = db.relationship("User", back_populates="authorships")
    # place = db.relationship("Place", back_populates="authorships")

    # def author_to_json(self):
    #     return {
    #         "author": self.user.to_jsonapi_dict(),
    #         "on": self.authorship_date
    #     }


# On crée notre modèle de document
class Document(db.Model):
    # document_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    # document_nom = db.Column(db.Text)
    # document_description = db.Column(db.Text)
    # document_longitude = db.Column(db.Float)
    # document_latitude = db.Column(db.Float)
    # document_type = db.Column(db.String(45))
    # authorships = db.relationship("Authorship", back_populates="document")

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
