from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Etudiant, Classe, Matiere, Note

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Page d'accueil"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard personnalisé selon le rôle"""
    
    if current_user.role == 'admin':
        # Statistiques pour l'admin
        total_etudiants = Etudiant.query.count()
        total_classes = Classe.query.count()
        total_matieres = Matiere.query.count()
        total_notes = Note.query.count()
        
        return render_template('dashboard.html',
                             total_etudiants=total_etudiants,
                             total_classes=total_classes,
                             total_matieres=total_matieres,
                             total_notes=total_notes)
    
    elif current_user.role == 'enseignant':
        # Statistiques pour l'enseignant
        total_etudiants = Etudiant.query.count()
        total_notes = Note.query.count()
        
        return render_template('dashboard.html',
                             total_etudiants=total_etudiants,
                             total_notes=total_notes)
    
    elif current_user.role == 'etudiant':
        # Informations pour l'étudiant
        # Trouver l'étudiant correspondant
        etudiant = Etudiant.query.filter_by(nom=current_user.nom, prenom=current_user.prenom).first()
        
        if etudiant:
            moyenne_generale = etudiant.calculer_moyenne_generale()
            credits_valides = etudiant.calculer_credits_valides()
            total_notes = len(etudiant.notes)
            
            return render_template('dashboard.html',
                                 etudiant=etudiant,
                                 moyenne_generale=moyenne_generale,
                                 credits_valides=credits_valides,
                                 total_notes=total_notes)
        
        return render_template('dashboard.html')
    
    return render_template('dashboard.html')
