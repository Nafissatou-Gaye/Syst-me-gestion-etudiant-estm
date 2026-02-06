import os

class Config:
    """Configuration de base pour l'application Flask"""
    
    # Clé secrète pour les sessions et CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise RuntimeError(
            "La variable d'environnement SECRET_KEY doit être définie pour sécuriser les sessions et la protection CSRF."
        )
    
    # Configuration de la base de données SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///gestion_etudiants.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration pour les uploads de fichiers
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    
    # Configuration pour le développement
    DEBUG = True
