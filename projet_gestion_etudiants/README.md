# 🎓 Système de Gestion des Étudiants

Application web Flask pour la gestion complète des étudiants, notes et bulletins.

## 📋 Fonctionnalités

### 👨‍💼 Administrateur
- ✅ Gestion des étudiants (CRUD)
- ✅ Gestion des classes
- ✅ Gestion des matières (coefficients et crédits)
- ✅ Gestion des filières (L1, L2, L3)
- ✅ Gestion des utilisateurs

### 👨‍🏫 Enseignant
- ✅ Saisie des notes
- ✅ Modification des notes
- ✅ Consultation des étudiants
- ✅ Historique des notes

### 👨‍🎓 Étudiant
- ✅ Consultation des notes
- ✅ Visualisation du bulletin
- ✅ Téléchargement du bulletin PDF
- ✅ Calcul automatique de la moyenne générale
- ✅ Suivi des crédits validés (60 crédits total)

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. **Cloner ou extraire le projet**
```bash
cd projet_gestion_etudiants
```

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python run.py
```

L'application sera accessible à l'adresse : `http://127.0.0.1:5000`

## 🌐 Accès Réseau Local

Pour que d'autres utilisateurs du réseau local puissent accéder à l'application :

1. **Trouver votre adresse IP locale**
   - Windows : `ipconfig`
   - Linux/Mac : `ifconfig` ou `ip addr`

2. **Les autres utilisateurs peuvent accéder via**
   ```
   http://VOTRE_IP:5000
   ```
   Exemple : `http://192.168.1.100:5000`

3. **Vérifier le pare-feu**
   Assurez-vous que le port 5000 est autorisé dans votre pare-feu.

## 👤 Comptes de Test

L'application est initialisée avec 3 comptes de test :

| Rôle | Login | Mot de passe |
|------|-------|--------------|
| Administrateur | `admin` | `admin123` |
| Enseignant | `enseignant` | `enseignant123` |
| Étudiant | `etudiant` | `etudiant123` |

## 📚 Matières et Crédits

Le système inclut 9 matières avec un total de 60 crédits :

| Matière | Coefficient | Crédits |
|---------|------------|---------|
| Algorithme | 3 | 8 |
| Base de données | 3 | 7 |
| Framework web | 2 | 6 |
| Réseau Telecom | 3 | 8 |
| Électronique | 2 | 6 |
| Gestion de projets | 2 | 6 |
| Anglais | 2 | 6 |
| Technique de communication | 2 | 6 |
| Droit | 2 | 7 |

## 🔧 Structure du Projet

```
projet_gestion_etudiants/
│
├── app/
│   ├── __init__.py          # Initialisation Flask
│   ├── models.py            # Modèles de base de données
│   ├── forms.py             # Formulaires WTForms
│   ├── utils.py             # Fonctions utilitaires
│   │
│   ├── routes/              # Routes de l'application
│   │   ├── auth.py          # Authentification
│   │   ├── admin.py         # Routes admin
│   │   ├── enseignant.py    # Routes enseignant
│   │   ├── etudiant.py      # Routes étudiant
│   │   └── main.py          # Routes principales
│   │
│   ├── templates/           # Templates HTML
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── admin/
│   │   ├── enseignant/
│   │   └── etudiant/
│   │
│   └── static/              # Fichiers statiques
│       ├── css/
│       ├── js/
│       └── img/
│
├── config.py                # Configuration
├── run.py                   # Point d'entrée
├── requirements.txt         # Dépendances
└── README.md               # Ce fichier
```

## 💾 Base de Données

L'application utilise SQLite par défaut. La base de données `gestion_etudiants.db` est créée automatiquement au premier lancement.

### Tables principales
- `utilisateur` - Comptes utilisateurs
- `etudiant` - Informations étudiants
- `classe` - Classes
- `matiere` - Matières
- `filiere` - Filières (L1, L2, L3)
- `note` - Notes des étudiants

## 🧮 Calculs Automatiques

### Moyenne par matière
Si plusieurs notes existent pour une matière, la moyenne arithmétique est calculée.

### Moyenne générale
Moyenne pondérée par les coefficients de chaque matière.

```
Moyenne = Σ(Note_matière × Coefficient) / Σ(Coefficients)
```

### Validation des crédits
Les crédits d'une matière sont validés si la moyenne de cette matière est ≥ 10/20.

## 📄 Génération de Bulletin PDF

Les étudiants peuvent télécharger leur bulletin au format PDF incluant :
- Informations personnelles
- Notes par matière avec coefficients
- Moyenne générale
- Crédits validés

## 🛠️ Technologies Utilisées

- **Backend** : Flask 3.0
- **ORM** : Flask-SQLAlchemy
- **Authentification** : Flask-Login
- **Formulaires** : Flask-WTF, WTForms
- **PDF** : ReportLab
- **Frontend** : Bootstrap 5, Font Awesome
- **Base de données** : SQLite

## 🔒 Sécurité

- Mots de passe hashés avec Werkzeug
- Protection CSRF avec Flask-WTF
- Contrôle d'accès par rôle
- Sessions sécurisées

## 📝 Notes de Développement

### Pour ajouter des données de test
```python
python
>>> from app import create_app, db
>>> from app.models import Etudiant, Classe
>>> app = create_app()
>>> with app.app_context():
...     # Vos opérations ici
```

### Pour réinitialiser la base de données
Supprimez le fichier `gestion_etudiants.db` et relancez l'application.

## 🎯 Améliorations Futures Possibles

- [ ] Export Excel des notes
- [ ] Envoi de bulletins par email
- [ ] Graphiques de statistiques
- [ ] Système de gestion des absences
- [ ] Calendrier des évaluations
- [ ] API REST pour intégration externe

## 👥 Auteur

Projet réalisé dans le cadre du cours de Licence 3 Réseaux et Télécommunications.

## 📄 Licence

Ce projet est à usage éducatif.

---

**Bonne chance avec votre projet ! 🚀**
