from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from app.models import Etudiant, Classe, Matiere, Filiere, Utilisateur
from app.forms import EtudiantForm, ClasseForm, MatiereForm, FiliereForm, UtilisateurForm
from app.utils import role_required, generer_matricule

bp = Blueprint('admin', __name__, url_prefix='/admin')

# ========== GESTION DES ÉTUDIANTS ==========

@bp.route('/etudiants')
@login_required
@role_required('admin')
def liste_etudiants():
    """Liste de tous les étudiants"""
    etudiants = Etudiant.query.all()
    return render_template('admin/etudiants.html', etudiants=etudiants)


@bp.route('/etudiant/ajouter', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def ajouter_etudiant():
    """Ajouter un nouvel étudiant"""
    form = EtudiantForm()
    
    # Charger les classes pour le SelectField
    form.classe_id.choices = [(0, 'Aucune')] + [(c.id, c.nom) for c in Classe.query.all()]
    
    if form.validate_on_submit():
        etudiant = Etudiant(
            matricule=form.matricule.data,
            nom=form.nom.data,
            prenom=form.prenom.data,
            date_naissance=form.date_naissance.data,
            email=form.email.data,
            telephone=form.telephone.data,
            classe_id=form.classe_id.data if form.classe_id.data != 0 else None
        )
        
        db.session.add(etudiant)
        db.session.commit()
        
        flash(f'Étudiant {etudiant.prenom} {etudiant.nom} ajouté avec succès !', 'success')
        return redirect(url_for('admin.liste_etudiants'))
    
    return render_template('admin/etudiant_form.html', form=form, titre='Ajouter un étudiant')


@bp.route('/etudiant/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def modifier_etudiant(id):
    """Modifier un étudiant existant"""
    etudiant = Etudiant.query.get_or_404(id)
    form = EtudiantForm(obj=etudiant)
    
    # Charger les classes pour le SelectField
    form.classe_id.choices = [(0, 'Aucune')] + [(c.id, c.nom) for c in Classe.query.all()]
    
    if form.validate_on_submit():
        etudiant.matricule = form.matricule.data
        etudiant.nom = form.nom.data
        etudiant.prenom = form.prenom.data
        etudiant.date_naissance = form.date_naissance.data
        etudiant.email = form.email.data
        etudiant.telephone = form.telephone.data
        etudiant.classe_id = form.classe_id.data if form.classe_id.data != 0 else None
        
        db.session.commit()
        
        flash(f'Étudiant {etudiant.prenom} {etudiant.nom} modifié avec succès !', 'success')
        return redirect(url_for('admin.liste_etudiants'))
    
    return render_template('admin/etudiant_form.html', form=form, titre='Modifier un étudiant', etudiant=etudiant)


@bp.route('/etudiant/supprimer/<int:id>')
@login_required
@role_required('admin')
def supprimer_etudiant(id):
    """Supprimer un étudiant"""
    etudiant = Etudiant.query.get_or_404(id)
    nom_complet = f"{etudiant.prenom} {etudiant.nom}"
    
    db.session.delete(etudiant)
    db.session.commit()
    
    flash(f'Étudiant {nom_complet} supprimé avec succès.', 'info')
    return redirect(url_for('admin.liste_etudiants'))


# ========== GESTION DES CLASSES ==========

@bp.route('/classes')
@login_required
@role_required('admin')
def liste_classes():
    """Liste de toutes les classes"""
    classes = Classe.query.all()
    return render_template('admin/classes.html', classes=classes)


@bp.route('/classe/ajouter', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def ajouter_classe():
    """Ajouter une nouvelle classe"""
    form = ClasseForm()
    
    # Charger les filières
    form.filiere_id.choices = [(0, 'Aucune')] + [(f.id, f'{f.nom} - {f.niveau}') for f in Filiere.query.all()]
    
    if form.validate_on_submit():
        classe = Classe(
            nom=form.nom.data,
            filiere_id=form.filiere_id.data if form.filiere_id.data != 0 else None
        )
        
        db.session.add(classe)
        db.session.commit()
        
        flash(f'Classe {classe.nom} ajoutée avec succès !', 'success')
        return redirect(url_for('admin.liste_classes'))
    
    return render_template('admin/classe_form.html', form=form, titre='Ajouter une classe')


@bp.route('/classe/supprimer/<int:id>')
@login_required
@role_required('admin')
def supprimer_classe(id):
    """Supprimer une classe"""
    classe = Classe.query.get_or_404(id)
    nom = classe.nom
    
    db.session.delete(classe)
    db.session.commit()
    
    flash(f'Classe {nom} supprimée avec succès.', 'info')
    return redirect(url_for('admin.liste_classes'))


# ========== GESTION DES MATIÈRES ==========

@bp.route('/matieres')
@login_required
@role_required('admin')
def liste_matieres():
    """Liste de toutes les matières"""
    matieres = Matiere.query.all()
    total_credits = sum(m.credit for m in matieres)
    return render_template('admin/matieres.html', matieres=matieres, total_credits=total_credits)


@bp.route('/matiere/ajouter', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def ajouter_matiere():
    """Ajouter une nouvelle matière"""
    form = MatiereForm()
    
    if form.validate_on_submit():
        matiere = Matiere(
            nom=form.nom.data,
            coefficient=form.coefficient.data,
            credit=form.credit.data,
            description=form.description.data
        )
        
        db.session.add(matiere)
        db.session.commit()
        
        flash(f'Matière {matiere.nom} ajoutée avec succès !', 'success')
        return redirect(url_for('admin.liste_matieres'))
    
    return render_template('admin/matiere_form.html', form=form, titre='Ajouter une matière')


@bp.route('/matiere/modifier/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def modifier_matiere(id):
    """Modifier une matière existante"""
    matiere = Matiere.query.get_or_404(id)
    form = MatiereForm(obj=matiere)
    
    if form.validate_on_submit():
        matiere.nom = form.nom.data
        matiere.coefficient = form.coefficient.data
        matiere.credit = form.credit.data
        matiere.description = form.description.data
        
        db.session.commit()
        
        flash(f'Matière {matiere.nom} modifiée avec succès !', 'success')
        return redirect(url_for('admin.liste_matieres'))
    
    return render_template('admin/matiere_form.html', form=form, titre='Modifier une matière', matiere=matiere)


@bp.route('/matiere/supprimer/<int:id>')
@login_required
@role_required('admin')
def supprimer_matiere(id):
    """Supprimer une matière"""
    matiere = Matiere.query.get_or_404(id)
    nom = matiere.nom
    
    db.session.delete(matiere)
    db.session.commit()
    
    flash(f'Matière {nom} supprimée avec succès.', 'info')
    return redirect(url_for('admin.liste_matieres'))


# ========== GESTION DES FILIÈRES ==========

@bp.route('/filieres')
@login_required
@role_required('admin')
def liste_filieres():
    """Liste de toutes les filières"""
    filieres = Filiere.query.all()
    return render_template('admin/filieres.html', filieres=filieres)


@bp.route('/filiere/ajouter', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def ajouter_filiere():
    """Ajouter une nouvelle filière"""
    form = FiliereForm()
    
    if form.validate_on_submit():
        filiere = Filiere(
            nom=form.nom.data,
            niveau=form.niveau.data,
            annee=form.annee.data
        )
        
        db.session.add(filiere)
        db.session.commit()
        
        flash(f'Filière {filiere.nom} - {filiere.niveau} ajoutée avec succès !', 'success')
        return redirect(url_for('admin.liste_filieres'))
    
    return render_template('admin/filiere_form.html', form=form, titre='Ajouter une filière')


# ========== GESTION DES UTILISATEURS ==========

@bp.route('/utilisateurs')
@login_required
@role_required('admin')
def liste_utilisateurs():
    """Liste de tous les utilisateurs"""
    utilisateurs = Utilisateur.query.all()
    return render_template('admin/utilisateurs.html', utilisateurs=utilisateurs)


@bp.route('/utilisateur/ajouter', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def ajouter_utilisateur():
    """Ajouter un nouvel utilisateur"""
    form = UtilisateurForm()
    
    if form.validate_on_submit():
        utilisateur = Utilisateur(
            nom=form.nom.data,
            prenom=form.prenom.data,
            login=form.login.data,
            role=form.role.data
        )
        utilisateur.set_password(form.password.data)
        
        db.session.add(utilisateur)
        db.session.commit()
        
        flash(f'Utilisateur {utilisateur.login} ajouté avec succès !', 'success')
        return redirect(url_for('admin.liste_utilisateurs'))
    
    return render_template('admin/utilisateur_form.html', form=form, titre='Ajouter un utilisateur')
