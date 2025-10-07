# Guide de Démarrage Rapide - Lazaristes

Ce guide vous permet de démarrer rapidement avec l'application Lazaristes.

## 🚀 Démarrage en 5 minutes

### Option 1 : Docker (Plus rapide)

```bash
# 1. Cloner le dépôt
git clone https://github.com/MatisseAD/lazaristes.git
cd lazaristes

# 2. Lancer avec Docker Compose
docker-compose up

# 3. Ouvrir dans votre navigateur
# http://localhost:5000
```

### Option 2 : Installation locale

```bash
# 1. Cloner le dépôt
git clone https://github.com/MatisseAD/lazaristes.git
cd lazaristes

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer l'application
python app.py

# 4. Ouvrir dans votre navigateur
# http://localhost:5000
```

## 📋 Fonctionnalités principales

### 1. Visualiser les commits récents
- La page d'accueil affiche automatiquement les 10 derniers commits
- Mise à jour automatique toutes les 30 secondes
- Affichage des statistiques du dépôt

### 2. Exécuter du code Python
1. Écrivez votre code dans l'éditeur de gauche
2. Cliquez sur "Exécuter le Code" ou utilisez `Ctrl+Enter`
3. Consultez la sortie dans le panneau de droite

**Exemple de code :**
```python
# Calculer les nombres de Fibonacci
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
```

### 3. Accéder aux ressources
- Notebooks explicatifs (ipynb)
- Scripts Python (.py)
- Liens directs vers les fichiers du dépôt

## 🔧 Configuration avancée

### Configurer les webhooks GitHub

1. **Générer un secret**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Configurer la variable d'environnement**
```bash
export WEBHOOK_SECRET="votre_secret_ici"
```

3. **Dans GitHub**
   - Settings > Webhooks > Add webhook
   - Payload URL: `https://votre-domaine.com/webhook`
   - Content type: `application/json`
   - Secret: (le secret généré à l'étape 1)

### Variables d'environnement disponibles

| Variable | Description | Défaut |
|----------|-------------|--------|
| `WEBHOOK_SECRET` | Secret pour valider les webhooks | (vide) |
| `FLASK_ENV` | Environnement Flask | `production` |

## 🧪 Tester l'installation

### Test de l'API

```bash
# Obtenir les statistiques
curl http://localhost:5000/api/stats

# Obtenir les commits
curl http://localhost:5000/api/commits

# Exécuter du code Python
curl -X POST http://localhost:5000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"code": "print(\"Hello from Lazaristes!\")"}'
```

### Test du sandboxing

Essayez ce code (il devrait échouer) :
```python
import os  # Devrait échouer - imports non autorisés
```

## 📱 Utilisation

### Interface principale

1. **Statistiques du dépôt** : En haut de la page
   - Total de commits
   - Nombre de fichiers
   - Fichiers Python et notebooks

2. **Liste des commits** : Section centrale
   - Hash du commit
   - Message
   - Auteur et date

3. **Exécuteur Python** : Section interactive
   - Éditeur de code à gauche
   - Sortie à droite
   - Boutons d'action en bas

4. **Ressources** : Section du bas
   - Liens vers notebooks
   - Liens vers scripts Python

### Raccourcis clavier

- `Ctrl+Enter` ou `Cmd+Enter` : Exécuter le code

## 🛠️ Dépannage rapide

### Le serveur ne démarre pas

```bash
# Vérifier que le port 5000 est libre
lsof -i :5000

# Si occupé, arrêter le processus ou changer le port
python app.py  # Le serveur utilise automatiquement le port 5000
```

### Les commits ne s'affichent pas

```bash
# Vérifier que Git est installé
git --version

# Vérifier que vous êtes dans un dépôt Git
git log -1
```

### Erreur de dépendances

```bash
# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

## 📚 Documentation complète

- [README.md](README.md) - Documentation principale
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide de déploiement complet
- [SECURITY.md](SECURITY.md) - Considérations de sécurité

## 💡 Exemples de code Python

### Exemple 1 : Analyse de liste
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Nombres pairs
pairs = [n for n in numbers if n % 2 == 0]
print(f"Nombres pairs: {pairs}")

# Somme des nombres impairs
impairs_sum = sum(n for n in numbers if n % 2 != 0)
print(f"Somme des impairs: {impairs_sum}")
```

### Exemple 2 : Fonction récursive
```python
def factorielle(n):
    if n <= 1:
        return 1
    return n * factorielle(n-1)

for i in range(1, 11):
    print(f"{i}! = {factorielle(i)}")
```

### Exemple 3 : Manipulation de chaînes
```python
texte = "Lazaristes Python"

print(f"Majuscules: {texte.upper()}")
print(f"Minuscules: {texte.lower()}")
print(f"Longueur: {len(texte)}")
print(f"Mots: {texte.split()}")
```

## 🎯 Prochaines étapes

1. **Explorez les notebooks** dans la section ressources
2. **Testez différents scripts Python** avec l'exécuteur
3. **Configurez les webhooks** pour les mises à jour automatiques
4. **Déployez en production** avec le guide de déploiement

## 🆘 Support

Si vous rencontrez des problèmes :

1. Consultez la [documentation complète](README.md)
2. Vérifiez les [problèmes connus](https://github.com/MatisseAD/lazaristes/issues)
3. Ouvrez une nouvelle issue sur GitHub

---

**Bon apprentissage avec Lazaristes! 🐍📚**
