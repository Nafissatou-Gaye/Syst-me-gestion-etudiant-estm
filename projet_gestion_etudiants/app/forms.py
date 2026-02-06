from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, ValidationError
from app.models import Utilisateur, Etudiant

class LoginForm(FlaskForm):
    """Formulaire de connexion"""
    login = StringField('Login', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Mot de passe', validators=[DataRequired()])


class EtudiantForm(FlaskForm):
    """Formulaire pour ajouter/modifier un étudiant"""
    matricule = StringField('Matricule', validators=[DataRequired(), Length(min=3, max=20)])
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=100)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=100)])
    date_naissance = DateField('Date de naissance', validators=[Optional()], format='%Y-%m-%d')
    email = StringField('Email', validators=[Optional(), Email()])
    telephone = StringField('Téléphone', validators=[Optional(), Length(max=20)])
    classe_id = SelectField('Classe', coerce=int, validators=[Optional()])
    
    def validate_matricule(self, matricule):
        """Vérifier que le matricule est unique"""
        etudiant = Etudiant.query.filter_by(matricule=matricule.data).first()
        if etudiant:
            raise ValidationError('Ce matricule existe déjà.')


class ClasseForm(FlaskForm):
    """Formulaire pour ajouter/modifier une classe"""
    nom = StringField('Nom de la classe', validators=[DataRequired(), Length(min=2, max=50)])
    filiere_id = SelectField('Filière', coerce=int, validators=[Optional()])


class MatiereForm(FlaskForm):
    """Formulaire pour ajouter/modifier une matière"""
    nom = StringField('Nom de la matière', validators=[DataRequired(), Length(min=2, max=100)])
    coefficient = IntegerField('Coefficient', validators=[DataRequired(), NumberRange(min=1, max=10)])
    credit = IntegerField('Crédits', validators=[DataRequired(), NumberRange(min=1, max=20)])
    description = TextAreaField('Description', validators=[Optional()])


class FiliereForm(FlaskForm):
    """Formulaire pour ajouter/modifier une filière"""
    nom = StringField('Nom de la filière', validators=[DataRequired(), Length(min=2, max=100)])
    niveau = SelectField('Niveau', choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')], validators=[DataRequired()])
    annee = IntegerField('Année', validators=[DataRequired()])


class NoteForm(FlaskForm):
    """Formulaire pour saisir une note"""
    etudiant_id = SelectField('Étudiant', coerce=int, validators=[DataRequired()])
    matiere_id = SelectField('Matière', coerce=int, validators=[DataRequired()])
    valeur = FloatField('Note', validators=[DataRequired(), NumberRange(min=0, max=20)])
    type_evaluation = SelectField('Type d\'évaluation', 
                                  choices=[('Devoir', 'Devoir'), 
                                          ('Examen', 'Examen'), 
                                          ('TP', 'TP'), 
                                          ('Projet', 'Projet')],
                                  validators=[Optional()])
    commentaire = TextAreaField('Commentaire', validators=[Optional()])


class UtilisateurForm(FlaskForm):
    """Formulaire pour ajouter/modifier un utilisateur"""
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=100)])
    prenom = StringField('Prénom', validators=[DataRequired(), Length(min=2, max=100)])
    login = StringField('Login', validators=[DataRequired(), Length(min=3, max=50)])
    role = SelectField('Rôle', 
                      choices=[('admin', 'Administrateur'), 
                              ('enseignant', 'Enseignant'), 
                              ('etudiant', 'Étudiant')],
                      validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    
    def validate_login(self, login):
        """Vérifier que le login est unique"""
        utilisateur = Utilisateur.query.filter_by(login=login.data).first()
        if utilisateur:
            raise ValidationError('Ce login existe déjà.')
