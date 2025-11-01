# Fonctionnalités - Lazaristes Dynamic Website

Ce document présente en détail toutes les fonctionnalités implémentées dans l'application Lazaristes.

## 🎯 Vue d'ensemble

L'application Lazaristes est un site web dynamique et interactif qui combine :
- **Visualisation en temps réel** des mises à jour du dépôt Git
- **Exécution sécurisée** de code Python dans le navigateur
- **Interface moderne** et responsive
- **Intégration GitHub** via webhooks

---

## 📊 1. Tableau de bord du dépôt

### Statistiques en temps réel

Le tableau de bord affiche quatre métriques clés :

1. **Total Commits** : Nombre total de commits dans le dépôt
2. **Total Fichiers** : Nombre de fichiers suivis par Git
3. **Fichiers Python** : Nombre de fichiers `.py`
4. **Notebooks** : Nombre de fichiers `.ipynb`

**Implémentation :**
- Endpoint API : `GET /api/stats`
- Mise à jour automatique : Toutes les 30 secondes
- Source : Commandes Git (`git rev-list --count HEAD`, `git ls-files`)

**Exemple de réponse API :**
```json
{
  "total_commits": "3",
  "total_files": 26,
  "python_files": 7,
  "notebook_files": 4,
  "status": "success"
}
```

### Liste des commits récents

Affiche les 10 derniers commits avec :
- Hash court du commit (7 caractères)
- Message du commit
- Nom de l'auteur
- Date et heure

**Caractéristiques :**
- Animation au survol (slide vers la droite)
- Code couleur avec bordure bleue
- Défilement si plus de 10 commits
- Rafraîchissement automatique

**Implémentation :**
- Endpoint API : `GET /api/commits`
- Source : `git log --pretty=format:%H|%an|%ae|%ad|%s -10`
- Format : JSON avec parsing côté serveur

---

## 💻 2. Exécuteur Python Interactif

### Interface d'édition de code

**Éditeur de code :**
- Zone de texte avec coloration syntaxique (thème sombre)
- Police monospace (`Courier New`)
- Redimensionnable verticalement
- Exemple de code préchargé

**Panneau de sortie :**
- Affichage en temps réel
- Thème sombre cohérent
- Défilement automatique pour longues sorties
- Préservation du formatage (whitespace, sauts de ligne)

### Fonctionnalités d'exécution

**Boutons d'action :**
1. **▶️ Exécuter le Code** (Ctrl+Enter)
   - Lance l'exécution du code
   - Affiche un état de chargement pendant l'exécution
   - Désactive le bouton pendant l'exécution

2. **🗑️ Effacer**
   - Vide l'éditeur de code
   - Réinitialise la sortie

**Messages de statut :**
- ✓ Code exécuté avec succès (vert)
- ✗ Erreur lors de l'exécution (rouge)
- Auto-disparition après 5 secondes

### Sécurité et sandboxing

**Environnement restreint :**

✅ **Fonctions autorisées :**
```python
# Affichage
print

# Types de base
str, int, float, bool

# Structures de données
list, dict, tuple, set

# Fonctions mathématiques
abs, max, min, sum, pow, round

# Itération et manipulation
len, range, sorted, reversed
enumerate, zip, map, filter
any, all
```

❌ **Fonctions interdites :**
```python
# Pas d'imports
import, __import__

# Pas d'accès fichiers
open, file

# Pas d'exécution dynamique
eval, exec, compile

# Pas d'accès système
os, sys, subprocess
```

**Protections supplémentaires :**
- Limite de taille : 10 000 caractères
- Rate limiting : 10 requêtes/minute par IP
- Timeout serveur : 120 secondes
- Isolation des sorties (stdout/stderr)

**Exemple de code sécurisé :**
```python
# ✅ Autorisé
numbers = [1, 2, 3, 4, 5]
sum_numbers = sum(numbers)
print(f"Somme : {sum_numbers}")

# ❌ Bloqué
import os  # ImportError
open('file.txt')  # NameError
```

---

## 🔄 3. Webhooks GitHub

### Configuration des webhooks

**Endpoint :** `POST /webhook`

**Validation de sécurité :**
- Signature HMAC-SHA256
- Vérification du secret
- Protection contre les replay attacks

**Événements supportés :**
- `push` : Nouveaux commits poussés
- `ping` : Test de webhook
- Autres événements (ignorés gracieusement)

**Exemple de configuration :**
```yaml
Payload URL: https://votre-domaine.com/webhook
Content type: application/json
Secret: <votre_secret_securise>
Events: Just the push event
```

### Traitement des événements

Lorsqu'un webhook est reçu :

1. **Validation de la signature**
   ```python
   expected = 'sha256=' + hmac.new(
       SECRET.encode(),
       request.data,
       hashlib.sha256
   ).hexdigest()
   ```

2. **Traitement de l'événement**
   - Logging de l'événement
   - Mise à jour potentielle des données (future amélioration)
   - Notification aux clients (via WebSocket - future amélioration)

3. **Réponse**
   - 200 OK : Événement traité
   - 401 Unauthorized : Signature invalide
   - 500 Error : Erreur serveur

---

## 🎨 4. Interface utilisateur

### Design moderne

**Palette de couleurs :**
- Primaire : Dégradé violet-bleu (#667eea → #764ba2)
- Secondaire : Blanc (#fff) pour le contenu
- Accent : Bleu (#667eea) pour les liens et titres
- Arrière-plan : Gris clair (#f8f9fa) pour les sections

**Typographie :**
- Police principale : Segoe UI, sans-serif
- Police monospace : Courier New (pour le code)
- Taille base : 16px
- Line height : 1.6

### Responsive Design

**Points de rupture :**
- Desktop : > 768px (grille 2 colonnes)
- Tablet/Mobile : ≤ 768px (grille 1 colonne)

**Adaptations mobiles :**
- Statistiques empilées verticalement
- Éditeur et sortie en colonne unique
- Navigation simplifiée
- Taille de texte adaptée

### Animations et transitions

**Effets interactifs :**
- Hover sur commits : Translation vers la droite (5px)
- Hover sur boutons : Changement de couleur
- Hover sur liens : Soulignement
- Loading spinner : Animation de rotation

**Transitions CSS :**
```css
transition: transform 0.2s;
transition: background 0.3s;
transition: color 0.2s;
```

---

## 🔌 5. API REST

### Endpoints disponibles

#### GET `/`
Sert la page HTML principale

**Réponse :** Page HTML

---

#### GET `/api/stats`
Statistiques du dépôt

**Réponse :**
```json
{
  "total_commits": "3",
  "total_files": 26,
  "python_files": 7,
  "notebook_files": 4,
  "status": "success"
}
```

---

#### GET `/api/commits`
Liste des derniers commits

**Paramètres :** Aucun

**Réponse :**
```json
{
  "commits": [
    {
      "hash": "7b5a141",
      "author": "Author Name",
      "email": "author@email.com",
      "date": "Tue Oct 7 12:45:29 2025 +0000",
      "message": "Commit message"
    }
  ],
  "status": "success"
}
```

---

#### GET `/api/files`
Fichiers modifiés récemment

**Réponse :**
```json
{
  "files": [
    {
      "status": "M",
      "filename": "app.py"
    },
    {
      "status": "A",
      "filename": "README.md"
    }
  ],
  "status": "success"
}
```

---

#### POST `/api/execute`
Exécuter du code Python

**Corps de la requête :**
```json
{
  "code": "print('Hello, World!')"
}
```

**Réponse (succès) :**
```json
{
  "output": "Hello, World!\n",
  "error": null,
  "status": "success"
}
```

**Réponse (erreur) :**
```json
{
  "output": "",
  "error": "NameError: name 'undefined_var' is not defined",
  "status": "error"
}
```

**Rate limiting :**
- 429 Too Many Requests si dépassement

---

#### POST `/webhook`
Récepteur de webhooks GitHub

**Headers requis :**
```
X-GitHub-Event: push
X-Hub-Signature-256: sha256=...
Content-Type: application/json
```

**Corps :** Payload GitHub

**Réponse :**
```json
{
  "message": "Webhook received",
  "event": "push",
  "status": "success"
}
```

---

## 🛡️ 6. Fonctionnalités de sécurité

### Protection contre les abus

1. **Rate Limiting**
   - 10 requêtes par minute par IP
   - Stockage en mémoire
   - Réponse 429 en cas de dépassement

2. **Validation des entrées**
   - Limite de taille du code (10 000 caractères)
   - Vérification du JSON
   - Échappement des sorties HTML

3. **CORS**
   - Configuration Flask-CORS
   - Permet les origines spécifiées
   - Headers sécurisés

4. **Webhook validation**
   - Signature HMAC-SHA256
   - Comparaison sûre (constant-time)
   - Rejet des requêtes non signées

### Sandboxing du code

**Méthode :**
- Dictionnaire `__builtins__` restreint
- Pas d'accès aux modules système
- Isolation des namespace

**Limitations :**
- Pas de timeout strict (amélioration future)
- Consommation mémoire non limitée
- Boucles infinies possibles (limité par timeout serveur)

---

## 🚀 7. Performance et optimisation

### Frontend

**Optimisations JavaScript :**
- Debouncing des requêtes
- Mise en cache côté client
- Chargement asynchrone
- Mise à jour partielle du DOM

**Optimisations CSS :**
- CSS inline pour réduire les requêtes
- Utilisation de CSS Grid et Flexbox
- Transitions GPU-accelerated

### Backend

**Optimisations Flask :**
- Réutilisation des processus Git
- Timeout configurables
- Workers Gunicorn multiples

**Recommandations production :**
```bash
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --timeout 120 \
         --worker-class sync \
         app:app
```

---

## 📱 8. Accessibilité

### Standards respectés

- Sémantique HTML5
- ARIA labels (future amélioration)
- Contraste suffisant (WCAG AA)
- Navigation au clavier

### Fonctionnalités d'accessibilité

- Raccourcis clavier (Ctrl+Enter)
- Messages de statut descriptifs
- Tailles de police lisibles
- Responsive pour tous les écrans

---

## 🔮 9. Améliorations futures

### Court terme

- [ ] WebSockets pour mises à jour en temps réel
- [ ] Timeout strict pour l'exécution Python
- [ ] Historique des exécutions
- [ ] Partage de code (liens courts)

### Moyen terme

- [ ] Authentification utilisateur
- [ ] Sauvegarde de code dans le navigateur
- [ ] Coloration syntaxique avancée (Monaco Editor)
- [ ] Support de plusieurs langages

### Long terme

- [ ] Collaboration en temps réel
- [ ] Notebooks interactifs
- [ ] Intégration avec Jupyter
- [ ] API publique avec clés

---

## 📊 10. Métriques et monitoring

### Métriques à surveiller

**Performance :**
- Temps de réponse API (< 200ms)
- Temps d'exécution Python (< 5s)
- Utilisation CPU/mémoire

**Utilisation :**
- Nombre d'exécutions par jour
- Taux d'erreur
- Taux de rate limiting

**Sécurité :**
- Tentatives d'exécution malveillante
- Webhooks invalides
- Dépassements de rate limit

### Outils recommandés

- **Logs** : stdout/stderr + fichiers
- **Monitoring** : Prometheus + Grafana
- **Alertes** : PagerDuty, Opsgenie
- **Uptime** : UptimeRobot, StatusPage

---

## 🎓 Cas d'usage

### Pour les étudiants

1. **Tester rapidement du code**
   - Pas besoin d'installation locale
   - Environnement prêt à l'emploi
   - Partage facile avec les profs

2. **Apprendre les algorithmes**
   - Exécution immédiate
   - Feedback visuel
   - Expérimentation sûre

3. **Accéder aux ressources**
   - Notebooks explicatifs
   - Scripts de cours
   - Exercices pratiques

### Pour les enseignants

1. **Démonstrations en direct**
   - Pas de configuration requise
   - Fonctionne sur tous les appareils
   - Accessible depuis n'importe où

2. **Partage de code**
   - URL unique
   - Toujours à jour
   - Versioning via Git

3. **Suivi des modifications**
   - Historique des commits
   - Notifications automatiques
   - Webhooks pour intégration

---

## 📸 Captures d'écran

### Page principale
![Page principale](https://github.com/user-attachments/assets/f626b796-4acb-422d-804a-63184eb22767)

### Exécution de code
![Exécution de code](https://github.com/user-attachments/assets/db593da5-b9aa-42ba-af00-ac7d4911dd87)

---

## 📚 Documentation complémentaire

- [README.md](README.md) - Installation et utilisation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Guide de déploiement
- [SECURITY.md](SECURITY.md) - Sécurité
- [QUICKSTART.md](QUICKSTART.md) - Démarrage rapide

---

**Version :** 1.0.0  
**Dernière mise à jour :** Octobre 2025
