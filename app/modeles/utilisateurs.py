from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.modeles.donnees import Person

#Création d'un classe pour le formulaire de connexion des utilisateurs. J'utilise
# le les formulaires flask pour vérifier que les données entrées par les utilisateurs
# correspondent aux données attendues
# DataRequired = indique que le champ ne peut pas être laissé vide par l'utilisateur
class LoginForm(FlaskForm):
    person_login = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    person_password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Connexion')

# Même chose pour la classe Registration = founit un modèle de formulaire pour
# l'enregistrement d'un nouvel utilisateur
class RegistrationForm(FlaskForm):
    person_firstName = StringField('Prénom<span style="color: #b21e1e;">*</span>', validators=[DataRequired()])
    person_name = StringField('Nom<span style="color: #b21e1e;">*</span>', validators=[DataRequired()])
    person_login = StringField('Nom d\'utilisateur<span style="color: #b21e1e;">*</span>', validators=[DataRequired()])
    person_email = StringField('Email<span style="color: #b21e1e;">*</span>', validators=[DataRequired(), Email()])
    person_password= PasswordField('Mot de passe<span style="color: #b21e1e;">*</span>', validators=[DataRequired()])
    password2 = PasswordField('Mot de passe<span style="color: #b21e1e;">*</span>', validators=[DataRequired(), EqualTo('person_password')])
    # password2 permet de vérifier le mot de passe pour éviter les erreurs de frappe
    person_git = StringField('Compte Github (URL)')
    person_linkedIn = StringField('Compte LinkedIn (URL)')
    person_promotion = StringField('Promotion TNAH (année du diplôme)')
    person_is_teacher = BooleanField('Je suis enseignant·e')
    submit = SubmitField('S\'enregistrer')

    def validate_username(self, person_login):
        user = Person.query.filter_by(person_login=Person.person_login.data).first()
        if user is not None:
            raise ValidationError('Nom d\'utilisateur déjà enregistré')
    def validate_email(self, person_email):
        user = Person.query.filter_by(person_email=Person.person_email.data).first()
        if user is not None:
            raise ValidationError('Adresse mail déjà enregistrée')

class EditProfileForm(FlaskForm):
    #formulaire pour la modification des infos utilisateur
    person_login = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    person_email = StringField('Email', validators=[DataRequired(), Email()])
    person_name = StringField('Nom', validators=[DataRequired()])
    person_firstName = StringField('Prénom', validators=[DataRequired()])
    person_promotion = StringField('Promotion (année du diplôme)')
    person_git = StringField('Compte GitHub (URL)')
    person_linkedIn= StringField('Compte LinkedIn (URL)')
    person_description = TextAreaField('Description')
    person_is_admin = BooleanField('ADMIN TNAHBox')
    submit = SubmitField('Enregistrer les modifications')


