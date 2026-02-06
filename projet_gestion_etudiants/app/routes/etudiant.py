from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app import db
from app.models import Etudiant, Note, Matiere
from app.utils import role_required
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import io
from datetime import datetime

bp = Blueprint('etudiant', __name__, url_prefix='/etudiant')

@bp.route('/mes-notes')
@login_required
@role_required('etudiant')
def mes_notes():
    """Afficher les notes de l'étudiant connecté"""
    # Trouver l'étudiant correspondant à l'utilisateur
    etudiant = Etudiant.query.filter_by(
        nom=current_user.nom,
        prenom=current_user.prenom
    ).first()
    
    if not etudiant:
        flash('Aucun profil étudiant trouvé pour cet utilisateur.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Grouper les notes par matière
    notes_par_matiere = {}
    for note in etudiant.notes:
        if note.matiere.nom not in notes_par_matiere:
            notes_par_matiere[note.matiere.nom] = {
                'matiere': note.matiere,
                'notes': [],
                'moyenne': 0
            }
        notes_par_matiere[note.matiere.nom]['notes'].append(note)
    
    # Calculer les moyennes par matière
    for matiere_nom, data in notes_par_matiere.items():
        notes_valeurs = [n.valeur for n in data['notes']]
        data['moyenne'] = round(sum(notes_valeurs) / len(notes_valeurs), 2) if notes_valeurs else 0
    
    moyenne_generale = etudiant.calculer_moyenne_generale()
    credits_valides = etudiant.calculer_credits_valides()
    
    return render_template('etudiant/mes_notes.html',
                         etudiant=etudiant,
                         notes_par_matiere=notes_par_matiere,
                         moyenne_generale=moyenne_generale,
                         credits_valides=credits_valides)


@bp.route('/bulletin')
@login_required
@role_required('etudiant')
def bulletin():
    """Afficher le bulletin de l'étudiant"""
    # Trouver l'étudiant correspondant
    etudiant = Etudiant.query.filter_by(
        nom=current_user.nom,
        prenom=current_user.prenom
    ).first()
    
    if not etudiant:
        flash('Aucun profil étudiant trouvé.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Grouper les notes par matière
    notes_par_matiere = {}
    for note in etudiant.notes:
        if note.matiere.nom not in notes_par_matiere:
            notes_par_matiere[note.matiere.nom] = {
                'matiere': note.matiere,
                'notes': [],
                'moyenne': 0,
                'valide': False
            }
        notes_par_matiere[note.matiere.nom]['notes'].append(note)
    
    # Calculer les moyennes et validation
    for matiere_nom, data in notes_par_matiere.items():
        notes_valeurs = [n.valeur for n in data['notes']]
        moyenne = sum(notes_valeurs) / len(notes_valeurs) if notes_valeurs else 0
        data['moyenne'] = round(moyenne, 2)
        data['valide'] = moyenne >= 10
    
    moyenne_generale = etudiant.calculer_moyenne_generale()
    credits_valides = etudiant.calculer_credits_valides()
    
    return render_template('etudiant/bulletin.html',
                         etudiant=etudiant,
                         notes_par_matiere=notes_par_matiere,
                         moyenne_generale=moyenne_generale,
                         credits_valides=credits_valides)


@bp.route('/bulletin/pdf')
@login_required
@role_required('etudiant')
def bulletin_pdf():
    """Générer et télécharger le bulletin en PDF"""
    # Trouver l'étudiant
    etudiant = Etudiant.query.filter_by(
        nom=current_user.nom,
        prenom=current_user.prenom
    ).first()
    
    if not etudiant:
        flash('Aucun profil étudiant trouvé.', 'warning')
        return redirect(url_for('main.dashboard'))
    
    # Créer le PDF en mémoire
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # En-tête
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 2*cm, "BULLETIN DE NOTES")
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 3*cm, "Année Universitaire 2024-2025")
    
    # Informations étudiant
    y = height - 5*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "Informations de l'étudiant")
    
    y -= 1*cm
    c.setFont("Helvetica", 12)
    c.drawString(2*cm, y, f"Nom: {etudiant.nom}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Prénom: {etudiant.prenom}")
    y -= 0.7*cm
    c.drawString(2*cm, y, f"Matricule: {etudiant.matricule}")
    y -= 0.7*cm
    if etudiant.classe:
        c.drawString(2*cm, y, f"Classe: {etudiant.classe.nom}")
        y -= 0.7*cm
    
    # Notes par matière
    y -= 1*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "Notes par matière")
    
    y -= 1*cm
    c.setFont("Helvetica", 10)
    
    # Grouper les notes
    notes_par_matiere = {}
    for note in etudiant.notes:
        if note.matiere.nom not in notes_par_matiere:
            notes_par_matiere[note.matiere.nom] = {
                'matiere': note.matiere,
                'notes': []
            }
        notes_par_matiere[note.matiere.nom]['notes'].append(note.valeur)
    
    # Afficher chaque matière
    for matiere_nom, data in sorted(notes_par_matiere.items()):
        moyenne = sum(data['notes']) / len(data['notes'])
        matiere = data['matiere']
        
        c.drawString(2*cm, y, f"{matiere_nom}")
        c.drawString(10*cm, y, f"Coef: {matiere.coefficient}")
        c.drawString(13*cm, y, f"Moyenne: {moyenne:.2f}/20")
        c.drawString(17*cm, y, f"Crédits: {matiere.credit if moyenne >= 10 else 0}/{matiere.credit}")
        
        y -= 0.7*cm
        
        if y < 3*cm:  # Nouvelle page si nécessaire
            c.showPage()
            y = height - 2*cm
            c.setFont("Helvetica", 10)
    
    # Résumé
    y -= 1*cm
    c.setFont("Helvetica-Bold", 14)
    c.drawString(2*cm, y, "Résumé")
    
    y -= 1*cm
    c.setFont("Helvetica", 12)
    moyenne_generale = etudiant.calculer_moyenne_generale()
    credits_valides = etudiant.calculer_credits_valides()
    
    c.drawString(2*cm, y, f"Moyenne générale: {moyenne_generale if moyenne_generale else 'N/A'}/20")
    y -= 0.8*cm
    c.drawString(2*cm, y, f"Crédits validés: {credits_valides}/60")
    
    # Pied de page
    c.setFont("Helvetica", 10)
    c.drawString(2*cm, 2*cm, f"Édité le {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
    
    c.save()
    
    buffer.seek(0)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'bulletin_{etudiant.matricule}.pdf'
    )
