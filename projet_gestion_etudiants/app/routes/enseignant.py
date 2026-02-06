from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Note, Etudiant, Matiere, Classe
from app.forms import NoteForm
from app.utils import role_required

bp = Blueprint('enseignant', __name__, url_prefix='/enseignant')

@bp.route('/notes')
@login_required
@role_required('enseignant')
def liste_notes():
    """Liste de toutes les notes"""
    notes = Note.query.order_by(Note.date_ajout.desc()).all()
    return render_template('enseignant/notes.html', notes=notes)


@bp.route('/note/ajouter', methods=['GET', 'POST'])
@login_required
@role_required('enseignant')
def ajouter_note():
    """Ajouter une nouvelle note"""
    form = NoteForm()
    
    # Charger les étudiants et matières pour les SelectField
    form.etudiant_id.choices = [(e.id, f'{e.matricule} - {e.prenom} {e.nom}') for e in Etudiant.query.all()]
    form.matiere_id.choices = [(m.id, m.nom) for m in Matiere.query.all()]
    
    if form.validate_on_submit():
        try:
            note = Note(
                etudiant_id=form.etudiant_id.data,
                matiere_id=form.matiere_id.data,
                valeur=form.valeur.data,
                type_evaluation=form.type_evaluation.data,
                commentaire=form.commentaire.data
            )
            
            db.session.add(note)
            db.session.commit()
            
            etudiant = Etudiant.query.get(form.etudiant_id.data)
            matiere = Matiere.query.get(form.matiere_id.data)
            
            flash(f'Note de {note.valeur}/20 ajoutée pour {etudiant.prenom} {etudiant.nom} en {matiere.nom}', 'success')
            return redirect(url_for('enseignant.liste_notes'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('enseignant/note_form.html', form=form, titre='Ajouter une note')


@bp.route('/note/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('enseignant')
def modifier_note(id):
    """Modifier une note existante"""
    note = Note.query.get_or_404(id)
    form = NoteForm(obj=note)
    
    # Charger les étudiants et matières
    form.etudiant_id.choices = [(e.id, f'{e.matricule} - {e.prenom} {e.nom}') for e in Etudiant.query.all()]
    form.matiere_id.choices = [(m.id, m.nom) for m in Matiere.query.all()]
    
    if form.validate_on_submit():
        try:
            note.etudiant_id = form.etudiant_id.data
            note.matiere_id = form.matiere_id.data
            note.valeur = form.valeur.data
            note.type_evaluation = form.type_evaluation.data
            note.commentaire = form.commentaire.data
            
            # Validation de la note
            if note.valeur < 0 or note.valeur > 20:
                raise ValueError("La note doit être entre 0 et 20")
            
            db.session.commit()
            
            flash('Note modifiée avec succès !', 'success')
            return redirect(url_for('enseignant.liste_notes'))
        
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('enseignant/note_form.html', form=form, titre='Modifier une note', note=note)


@bp.route('/note/supprimer/<int:id>')
@login_required
@role_required('enseignant')
def supprimer_note(id):
    """Supprimer une note"""
    note = Note.query.get_or_404(id)
    
    db.session.delete(note)
    db.session.commit()
    
    flash('Note supprimée avec succès.', 'info')
    return redirect(url_for('enseignant.liste_notes'))


@bp.route('/classe/<int:classe_id>/notes')
@login_required
@role_required('enseignant')
def notes_par_classe(classe_id):
    """Afficher les notes d'une classe"""
    classe = Classe.query.get_or_404(classe_id)
    etudiants = classe.etudiants
    
    return render_template('enseignant/notes_classe.html', classe=classe, etudiants=etudiants)


@bp.route('/etudiants')
@login_required
@role_required('enseignant')
def liste_etudiants():
    """Liste des étudiants pour l'enseignant"""
    etudiants = Etudiant.query.all()
    return render_template('enseignant/etudiants.html', etudiants=etudiants)
