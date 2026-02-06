from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    """Charger un utilisateur pour Flask-Login"""
    return Utilisateur.query.get(int(user_id))

class Utilisateur(UserMixin, db.Model):
    """Modèle pour les utilisateurs (Admin, Enseignant, Étudiant)"""
    __tablename__ = 'utilisateur'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, enseignant, etudiant
    motdepasse_hash = db.Column(db.String(200), nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Hasher le mot de passe"""
        self.motdepasse_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifier le mot de passe"""
        return check_password_hash(self.motdepasse_hash, password)
    
    def __repr__(self):
        return f'<Utilisateur {self.login} - {self.role}>'


class Filiere(db.Model):
    """Modèle pour les filières (L1, L2, L3)"""
    __tablename__ = 'filiere'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    niveau = db.Column(db.String(10), nullable=False)  # L1, L2, L3
    annee = db.Column(db.Integer, nullable=False)
    
    # Relations
    classes = db.relationship('Classe', backref='filiere', lazy=True)
    
    def __repr__(self):
        return f'<Filiere {self.nom} - {self.niveau}>'


class Classe(db.Model):
    """Modèle pour les classes"""
    __tablename__ = 'classe'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    filiere_id = db.Column(db.Integer, db.ForeignKey('filiere.id'), nullable=True)
    
    # Relations
    etudiants = db.relationship('Etudiant', backref='classe', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Classe {self.nom}>'


class Etudiant(db.Model):
    """Modèle pour les étudiants"""
    __tablename__ = 'etudiant'
    
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=True)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    notes = db.relationship('Note', backref='etudiant', lazy=True, cascade='all, delete-orphan')
    
    def calculer_moyenne_generale(self):
        """Calculer la moyenne générale pondérée"""
        if not self.notes:
            return None
        
        total_notes = 0
        total_coefficients = 0
        
        # Grouper les notes par matière
        notes_par_matiere = {}
        for note in self.notes:
            if note.matiere_id not in notes_par_matiere:
                notes_par_matiere[note.matiere_id] = []
            notes_par_matiere[note.matiere_id].append(note.valeur)
        
        # Calculer la moyenne par matière puis la moyenne générale
        for matiere_id, valeurs in notes_par_matiere.items():
            matiere = Matiere.query.get(matiere_id)
            moyenne_matiere = sum(valeurs) / len(valeurs)
            total_notes += moyenne_matiere * matiere.coefficient
            total_coefficients += matiere.coefficient
        
        if total_coefficients == 0:
            return None
        
        return round(total_notes / total_coefficients, 2)
    
    def calculer_credits_valides(self):
        """Calculer le total des crédits validés (note >= 10)"""
        credits_valides = 0
        
        # Grouper les notes par matière
        notes_par_matiere = {}
        for note in self.notes:
            if note.matiere_id not in notes_par_matiere:
                notes_par_matiere[note.matiere_id] = []
            notes_par_matiere[note.matiere_id].append(note.valeur)
        
        # Vérifier si la moyenne de chaque matière >= 10
        for matiere_id, valeurs in notes_par_matiere.items():
            moyenne_matiere = sum(valeurs) / len(valeurs)
            if moyenne_matiere >= 10:
                matiere = Matiere.query.get(matiere_id)
                credits_valides += matiere.credit
        
        return credits_valides
    
    def __repr__(self):
        return f'<Etudiant {self.matricule} - {self.prenom} {self.nom}>'


class Matiere(db.Model):
    """Modèle pour les matières"""
    __tablename__ = 'matiere'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False, unique=True)
    coefficient = db.Column(db.Integer, nullable=False, default=1)
    credit = db.Column(db.Integer, nullable=False, default=5)
    description = db.Column(db.Text, nullable=True)
    
    # Relations
    notes = db.relationship('Note', backref='matiere', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Matiere {self.nom}>'


class Note(db.Model):
    """Modèle pour les notes"""
    __tablename__ = 'note'
    
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiant.id'), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)
    valeur = db.Column(db.Float, nullable=False)
    type_evaluation = db.Column(db.String(50), nullable=True)  # Devoir, Examen, TP, etc.
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)
    commentaire = db.Column(db.Text, nullable=True)
    
    def __init__(self, **kwargs):
        super(Note, self).__init__(**kwargs)
        # Validation : note entre 0 et 20
        if self.valeur < 0 or self.valeur > 20:
            raise ValueError("La note doit être entre 0 et 20")
    
    def __repr__(self):
        return f'<Note {self.valeur}/20 - Étudiant {self.etudiant_id} - Matière {self.matiere_id}>'
