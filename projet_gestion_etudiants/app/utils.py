from app import db
from app.models import Utilisateur, Matiere, Filiere, Classe
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def init_data():
    """Initialiser la base de données avec des données de base"""
    
    # Vérifier si des données existent déjà
    if Utilisateur.query.first():
        return
    
    # Créer un administrateur par défaut
    admin = Utilisateur(
        nom='Admin',
        prenom='Système',
        login='admin',
        role='admin'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Créer un enseignant par défaut
    enseignant = Utilisateur(
        nom='Diop',
        prenom='Mamadou',
        login='enseignant',
        role='enseignant'
    )
    enseignant.set_password('enseignant123')
    db.session.add(enseignant)
    
    # Créer un étudiant par défaut
    etudiant = Utilisateur(
        nom='Ndiaye',
        prenom='Fatou',
        login='etudiant',
        role='etudiant'
    )
    etudiant.set_password('etudiant123')
    db.session.add(etudiant)
    
    # Créer les filières
    filieres_data = [
        {'nom': 'Réseaux et Télécommunications', 'niveau': 'L1', 'annee': 2024},
        {'nom': 'Réseaux et Télécommunications', 'niveau': 'L2', 'annee': 2024},
        {'nom': 'Réseaux et Télécommunications', 'niveau': 'L3', 'annee': 2024},
    ]
    
    for f in filieres_data:
        filiere = Filiere(**f)
        db.session.add(filiere)
    
    # Créer les matières avec crédits (total = 60)
    matieres_data = [
        {'nom': 'Algorithme', 'coefficient': 3, 'credit': 8},
        {'nom': 'Base de données', 'coefficient': 3, 'credit': 7},
        {'nom': 'Framework web', 'coefficient': 2, 'credit': 6},
        {'nom': 'Réseau Telecom', 'coefficient': 3, 'credit': 8},
        {'nom': 'Électronique', 'coefficient': 2, 'credit': 6},
        {'nom': 'Gestion de projets', 'coefficient': 2, 'credit': 6},
        {'nom': 'Anglais', 'coefficient': 2, 'credit': 6},
        {'nom': 'Technique de communication', 'coefficient': 2, 'credit': 6},
        {'nom': 'Droit', 'coefficient': 2, 'credit': 7},
    ]
    
    for m in matieres_data:
        matiere = Matiere(**m)
        db.session.add(matiere)
    
    # Créer quelques classes
    classes_data = [
        {'nom': 'L1 RT Groupe A'},
        {'nom': 'L2 RT Groupe A'},
        {'nom': 'L3 RT Groupe A'},
    ]
    
    for c in classes_data:
        classe = Classe(**c)
        db.session.add(classe)
    
    db.session.commit()
    print("Base de données initialisée avec succès!")


def role_required(role):
    """Décorateur pour vérifier le rôle de l'utilisateur"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Veuillez vous connecter.', 'danger')
                return redirect(url_for('auth.login'))
            
            if current_user.role != role:
                flash('Vous n\'avez pas accès à cette page.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def generer_matricule():
    """Générer un matricule unique pour un étudiant"""
    from app.models import Etudiant
    import random
    import string
    
    annee = 2024
    while True:
        # Format: 2024XXXXX (année + 5 chiffres aléatoires)
        numero = ''.join(random.choices(string.digits, k=5))
        matricule = f"{annee}{numero}"
        
        # Vérifier l'unicité
        if not Etudiant.query.filter_by(matricule=matricule).first():
            return matricule
