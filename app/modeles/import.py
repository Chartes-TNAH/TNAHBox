from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app.modeles.donnees import Document

# Création d'une classe pour le formulaire d'import des documents
# utilisation formulaires flask pour vérifier que les données entrées par les utilisateurs correspondent aux données attendues
# même idée que pour utilisateurs.py et page inscription.html
# DataRequired = indique que le champ ne peut pas être laissé vide par l'utilisateur
class ImportForm(FlaskForm):
    document_title = StringField('Titre<span style="color: red;">*</span>', validators=[DataRequired()])
    document_description = StringField('Description<span style="color: red;">*</span>', validators=[DataRequired()])
    document_format = StringField('Format<span style="color: red;">*</span>', validators=[DataRequired()])
    document_date = StringField('Date<span style="color: red;">*</span>', validators=[DataRequired()])
    document_teaching = StringField('Matière<span style="color: red;">*</span>', validators=[DataRequired()])
    document_downloadLink = StringField('Lien de téléchargement<span style="color: red;">*</span>', validators=[DataRequired()])
    submit = SubmitField('Importer')


    #def validate_username(self, person_login):
     #   user = Person.query.filter_by(person_login=Person.person_login.data).first()
      #  if user is not None:
       #     raise ValidationError('Nom d\'utilisateur déjà enregistré')
    #def validate_email(self, person_email):
     #   user = Person.query.filter_by(person_email=Person.person_email.data).first()
      #  if user is not None:
       #     raise ValidationError('Adresse mail déjà enregistrée')