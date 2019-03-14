from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from app.modeles.donnees import Person

#Création d'un classe pour le formulaire de connexion des utilisateurs. J'utilise
# le les formulaires flask pour vérifier que les données entrées par les utilisateurs
# correspondent aux données attendues
# DataRequired = indique que le champ ne peut pas être laissé vide par l'utilisateur
class LoginForm(FlaskForm):
    person_login = StringField('Nom utilisateur', validators=[DataRequired()])
    person_password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

# Même chose pour la classe Registration = founit un modèle de formulaire pour
# l'enregistrement d'un nouvel utilisateur
class RegistrationForm(FlaskForm):
    person_firstName = StringField('Prénom*', validators=[DataRequired()])
    person_name = StringField('Nom*', validators=[DataRequired()])
    person_login = StringField('Nom d\'utilisateur*', validators=[DataRequired()])
    person_email = StringField('Email*', validators=[DataRequired(), Email()])
    person_password= PasswordField('Mot de passe*', validators=[DataRequired()])
    password2 = PasswordField('Mot de passe*', validators=[DataRequired(), EqualTo('person_password')])
    # password2 permet de vérifier le mot de passe pour éviter les erreurs de frappe
    person_git = StringField('Compte Github (URL)')
    person_linkedIn = StringField('Compte LinkedIn (URL)')
    person_promotion = StringField('Promotion TNAH')
    submit = SubmitField('S\'enregistrer')

    def validate_username(self, person_login):
        user = Person.query.filter_by(person_login=Person.person_login.data).first()
        if user is not None:
            raise ValidationError('Nom d\'utilisateur déjà enregistré')
    def validate_email(self, person_email):
        user = Person.query.filter_by(person_email=Person.person_email.data).first()
        if user is not None:
            raise ValidationError('Adresse mail déjà enregistrée')


