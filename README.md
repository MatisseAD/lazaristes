# Lazaristes - Ressources Python pour la Prépa

Site web dynamique et interactif pour les ressources Python destinées aux étudiants en classes préparatoires.

## 🌟 Fonctionnalités

### 1. **Mises à jour automatiques du dépôt**
- Détection automatique des nouveaux commits
- Affichage dynamique des fichiers ajoutés/modifiés
- Statistiques en temps réel du dépôt
- Rafraîchissement automatique toutes les 30 secondes

### 2. **Exécution de code Python en ligne**
- Interface d'édition de code intégrée
- Exécution sécurisée dans un environnement sandboxé
- Affichage de la sortie en temps réel
- Limitation de taux pour prévenir les abus
- Raccourci clavier : Ctrl+Enter pour exécuter

### 3. **Interface utilisateur moderne**
- Design responsive (mobile, tablette, desktop)
- Interface claire et intuitive
- Thème visuel attrayant avec dégradés
- Sections bien organisées pour les ressources

### 4. **Support des Webhooks GitHub**
- Écoute des événements GitHub (push, commits, etc.)
- Validation HMAC des signatures webhook
- Déclenchement automatique des mises à jour

## 🚀 Installation et Déploiement

### Méthode 1 : Avec Docker (Recommandé)

#### Prérequis
- Docker
- Docker Compose

#### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/MatisseAD/lazaristes.git
cd lazaristes
```

2. **Construire et lancer avec Docker Compose**
```bash
docker-compose up --build
```

3. **Accéder au site**
Ouvrez votre navigateur et allez sur : `http://localhost:5000`

### Méthode 2 : Installation locale

#### Prérequis
- Python 3.8 ou supérieur
- pip

#### Étapes

1. **Cloner le dépôt**
```bash
git clone https://github.com/MatisseAD/lazaristes.git
cd lazaristes
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python app.py
```

5. **Accéder au site**
Ouvrez votre navigateur et allez sur : `http://localhost:5000`

### Méthode 3 : Déploiement en production avec Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

## 🔧 Configuration

### Variables d'environnement

| Variable | Description | Valeur par défaut |
|----------|-------------|-------------------|
| `WEBHOOK_SECRET` | Secret pour valider les webhooks GitHub | (vide) |
| `FLASK_ENV` | Environnement Flask | `production` |
| `FLASK_APP` | Fichier principal de l'application | `app.py` |

### Configuration des Webhooks GitHub

Pour activer les mises à jour automatiques via webhooks :

1. **Aller dans les paramètres du dépôt GitHub**
   - Accédez à `Settings` > `Webhooks` > `Add webhook`

2. **Configurer le webhook**
   - **Payload URL** : `https://votre-domaine.com/webhook`
   - **Content type** : `application/json`
   - **Secret** : Générez un secret sécurisé et ajoutez-le dans la variable d'environnement `WEBHOOK_SECRET`
   - **Events** : Sélectionnez "Just the push event" ou "Send me everything"

3. **Sauvegarder**

4. **Tester le webhook**
   GitHub enverra un événement de test que vous pourrez vérifier dans l'onglet "Recent Deliveries"

### Exemple de configuration du secret

**Linux/Mac:**
```bash
export WEBHOOK_SECRET="votre_secret_securise_ici"
```

**Windows:**
```cmd
set WEBHOOK_SECRET=votre_secret_securise_ici
```

**Docker Compose:**
Créez un fichier `.env` à la racine :
```env
WEBHOOK_SECRET=votre_secret_securise_ici
```

## 🔒 Sécurité

### Sandboxing du code Python

L'exécution de code Python est sécurisée via :

1. **Environnement restreint** : Seules les fonctions built-in sûres sont disponibles
2. **Limitation de taux** : Maximum 10 requêtes par minute par IP
3. **Limitation de taille** : Code limité à 10 000 caractères
4. **Pas d'accès aux ressources système** : Pas d'import de modules, pas d'accès aux fichiers

### Fonctions Python autorisées

- Fonctions de base : `print`, `len`, `range`, `str`, `int`, `float`, etc.
- Structures de données : `list`, `dict`, `tuple`, `set`
- Fonctions mathématiques : `abs`, `max`, `min`, `sum`, `pow`, `round`
- Fonctions d'itération : `sorted`, `reversed`, `enumerate`, `zip`, `map`, `filter`

### Recommandations de sécurité

1. **Ne jamais exposer le secret webhook** dans le code source
2. **Utiliser HTTPS** en production
3. **Configurer un reverse proxy** (nginx/Apache) avec SSL
4. **Limiter l'accès réseau** du conteneur Docker
5. **Surveiller les logs** pour détecter les abus

## 📁 Structure du projet

```
lazaristes/
├── app.py                      # Application Flask principale
├── docs/
│   └── index.html             # Page web principale
├── requirements.txt           # Dépendances Python
├── Dockerfile                 # Configuration Docker
├── docker-compose.yml         # Configuration Docker Compose
├── README.md                  # Ce fichier
├── chapitre2.py              # Scripts Python du cours
├── chapitre3.py
├── chapitre4.py
├── TP02.py
├── TP03.py
├── *.ipynb                    # Notebooks Jupyter
└── .gitignore
```

## 🛠️ Développement

### Lancer en mode développement

```bash
export FLASK_ENV=development
python app.py
```

Le serveur se rechargera automatiquement lors des modifications de code.

### Tests locaux

1. **Tester l'exécution de code Python** :
   - Accédez à `http://localhost:5000`
   - Utilisez l'éditeur de code pour tester différents scripts

2. **Tester les API endpoints** :
```bash
# Obtenir les statistiques du dépôt
curl http://localhost:5000/api/stats

# Obtenir les commits récents
curl http://localhost:5000/api/commits

# Exécuter du code Python
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello, World!\")"}'
```

## 📊 API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Page principale |
| `/api/stats` | GET | Statistiques du dépôt |
| `/api/commits` | GET | Liste des 10 derniers commits |
| `/api/files` | GET | Fichiers modifiés récemment |
| `/api/execute` | POST | Exécuter du code Python |
| `/webhook` | POST | Récepteur de webhooks GitHub |

## 🐛 Dépannage

### Le serveur ne démarre pas

- Vérifiez que le port 5000 n'est pas déjà utilisé
- Vérifiez que toutes les dépendances sont installées
- Consultez les logs : `docker-compose logs -f`

### Les commits ne s'affichent pas

- Assurez-vous que Git est installé et configuré
- Vérifiez que le dépôt a bien un historique Git
- Consultez la console du navigateur pour les erreurs JavaScript

### L'exécution de code ne fonctionne pas

- Vérifiez que le serveur Flask est en cours d'exécution
- Vérifiez les CORS si vous utilisez un domaine différent
- Consultez la console du navigateur et les logs du serveur

### Les webhooks ne fonctionnent pas

- Vérifiez que `WEBHOOK_SECRET` est correctement configuré
- Assurez-vous que l'URL du webhook est accessible publiquement
- Vérifiez les logs de livraison dans GitHub

## 📝 Licence

Ce projet est destiné à des fins éducatives pour les étudiants en classes préparatoires.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir des issues pour signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📧 Contact

Pour toute question ou suggestion, ouvrez une issue sur GitHub.

---

**Note** : Ce site est conçu pour être utilisé dans un environnement éducatif. L'exécution de code Python est sandboxée mais doit être utilisée de manière responsable.
