from .. app import db


class HasTag(db.Model):
    tagged_document_id = db.Column(db.Integer, db.ForeignKey('Document.document_id'), primary_key=True)
    document_tag_id = db.Column(db.Integer, db.ForeignKey('Tag.tag_id'), primary_key=True)

class Authorship(db.Model):
    author_of_document_id = db.Column(db.Integer, db.ForeignKey('Person.person_id'), primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('Document.document_id'), primary_key=True)

class Document(db.Model):
    document_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    document_title = db.Column(db.Text)
    document_description = db.Column(db.Text)
    document_format = db.Column(db.String)
    document_date = db.Column(db.Text)
    document_teaching = db.Column(db.String)
    document_downloadLink = db.Column(db.Text)
    document_tag = db.relationship("Tag",
                    secondary=HasTag,
                    back_populates="tagged_document")
    document_author = db.relationship("Person",
                    secondary=Authorship,
                    back_populates="created_document")

class Tag(db.Model):
    tag_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    tag_label = db.Column(db.String, nullable=False)
    tagged_document = db.relationship("Document",
                    secondary=HasTag,
                    back_populates="document_tag")

class Person(db.Model):
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
                    back_populates="document_author")

    def __repr__(self):
        return '<User {}>'.format(self.person_login)