from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField, ValidationError
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
    document_format = RadioField('Format<span style="color: red;">*</span>', choices=[('Image'),('Texte'),('Code'),('Autre')])
    document_date = StringField('Date<span style="color: red;">*</span>')
    document_teaching = SelectField('Matière<span style="color: red;">*</span>', choices=[('XML-TEI'),('XML-EAD'),('Python'),('Omeka'),('Algo'),('HTML'),('JavaScript'),('Git'),('LaTeX'),('Linux'),('Regex'),('Xquery'),('XSLT'),('Référencement'),('Data'),('Autre')])
    document_downloadLink = StringField('Lien de téléchargement<span style="color: red;">*</span>', validators=[DataRequired()])
    submit = SubmitField('Importer')

#le RadioField permet de cocher des éléments, se prête particulièrement bien à l'exercice pour
# les formats de documents, qui sont au nombre de 4 : timage, texte, code, autre
#le SelectField doit donner un menu déroulant
#SubmitField : aucune idée
