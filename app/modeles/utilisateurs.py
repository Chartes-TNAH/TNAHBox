from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app.modeles.donnees import Person

#Création d'un classe pour le formulaire de connexion des utilisateurs. J'utilise
# le les formulaires flask pour vérifier que les données entrées par les utilisateurs
# correspondent aux données attendues
# DataRequired = indique que le champ ne peut pas être laissé vide par l'utilisateur
class LoginForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

# Même chose pour la classe Registration = founit un modèle de formulaire pour
# l'enregistrement d'un nouvel utilisateur
class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email])
    password= PasswordField('Mot de passe', validators=[DataRequired()])
    password2 = PasswordField('Mot de passe', validators=[DataRequired(), EqualTo('password')])
    # password2 permet de vérifier le mot de passe pour éviter les erreurs de frappe
    github = StringField('Compte Github (URL)')
    linkedin = StringField('Compte LinkedIn (URL)')
    promotion = StringField('Promotion TNAH')
    submit = SubmitField('S\'enreistrer')

    def validate_username(self, username):
        user = Person.query.filter_by(username=Person.person_login.data).first()
        if user is not None:
            raise ValidationError('Nom d\'utilisateur déjà enregistré')
    def validate_email(self, email):
        user = Person.query.filter_by(email=Person.person_email.data).first()
        if user is not None:
            raise ValidationError('Adresse mail déjà enregistrée')


