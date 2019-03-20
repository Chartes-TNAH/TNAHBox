from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app.modeles.donnees import Document


# JE NE M'EXPLIQUE PAS POURQUOI CETTE LIGNE APPARAIT EN GRISE
# , se comporte come si il ne savait reconnaître la classe Document ; va peut-être poser problème

# Création d'une classe pour le formulaire d'import des documents
# utilisation formulaires flask pour vérifier que les données entrées par les utilisateurs
# correspondent aux données attendues
# même idée que pour utilisateurs.py et page inscription.html
# DataRequired = indique que le champ ne peut pas être laissé vide par l'utilisateur


class ImportForm(FlaskForm):
    document_title = StringField('Titre<span style="color: red;">*</span>', validators=[DataRequired()])
    document_description = StringField('Description<span style="color: red;">*</span>', validators=[DataRequired()])
    document_format = StringField('Format<span style="color: red;">*</span>', validators=[DataRequired()])
    document_date = StringField('Date<span style="color: red;">*</span>')
    document_teaching = StringField('Matière<span style="color: red;">*</span>', validators=[DataRequired()])
    document_downloadLink = StringField('Lien de téléchargement<span style="color: red;">*</span>', validators=[DataRequired()])
    submit = SubmitField('Importer')

