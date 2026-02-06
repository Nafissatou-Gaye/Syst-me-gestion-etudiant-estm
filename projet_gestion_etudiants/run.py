from app import create_app, db
from app.models import Utilisateur, Classe, Etudiant, Matiere, Filiere, Note

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Rendre les modèles disponibles dans le shell Flask"""
    return {
        'db': db, 
        'Utilisateur': Utilisateur, 
        'Classe': Classe,
        'Etudiant': Etudiant,
        'Matiere': Matiere,
        'Filiere': Filiere,
        'Note': Note
    }

if __name__ == '__main__':
    # Configuration pour accès réseau local
    # Ton serveur sera accessible via http://TON_IP:5000
    # Pour trouver ton IP: 
    # - Windows: ipconfig
    # - Linux/Mac: ifconfig ou ip addr
    app.run(host='0.0.0.0', port=5000, debug=True)
