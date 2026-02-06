from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialisation des extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialiser les extensions avec l'app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
    login_manager.login_message_category = 'info'
    
    # Enregistrer les blueprints (routes)
    from app.routes import auth, admin, enseignant, etudiant, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(enseignant.bp)
    app.register_blueprint(etudiant.bp)
    app.register_blueprint(main.bp)
    
    # Créer les tables de la base de données
    with app.app_context():
        db.create_all()
        
        # Importer la fonction d'initialisation
        from app.utils import init_data
        init_data()
    
    return app
