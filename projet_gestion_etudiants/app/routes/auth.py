from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from app import db
from app.models import Utilisateur
from app.forms import LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        utilisateur = Utilisateur.query.filter_by(login=form.login.data).first()
        
        if utilisateur and utilisateur.check_password(form.password.data):
            login_user(utilisateur)
            flash(f'Bienvenue {utilisateur.prenom} {utilisateur.nom} !', 'success')
            
            # Rediriger vers la page demandée ou dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login ou mot de passe incorrect.', 'danger')
    
    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('auth.login'))
