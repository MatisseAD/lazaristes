# Guide de Déploiement - Lazaristes

Ce guide détaille les différentes options de déploiement pour l'application Lazaristes.

## Table des matières

1. [Déploiement sur un serveur VPS](#déploiement-sur-un-serveur-vps)
2. [Déploiement sur Heroku](#déploiement-sur-heroku)
3. [Déploiement sur Railway](#déploiement-sur-railway)
4. [Déploiement sur DigitalOcean App Platform](#déploiement-sur-digitalocean)
5. [Déploiement sur AWS EC2](#déploiement-sur-aws-ec2)
6. [Configuration GitHub Pages avec API Backend](#github-pages-avec-backend)

---

## Déploiement sur un serveur VPS

### Prérequis
- Un serveur VPS (Ubuntu 20.04+ recommandé)
- Accès SSH
- Nom de domaine (optionnel mais recommandé)

### Étape 1 : Configuration initiale du serveur

```bash
# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation des dépendances
sudo apt install -y python3 python3-pip python3-venv nginx git
```

### Étape 2 : Cloner le projet

```bash
# Créer un utilisateur pour l'application
sudo useradd -m -s /bin/bash lazaristes
sudo su - lazaristes

# Cloner le dépôt
git clone https://github.com/MatisseAD/lazaristes.git
cd lazaristes
```

### Étape 3 : Configuration de l'environnement Python

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 4 : Configuration systemd

Créer un fichier service : `/etc/systemd/system/lazaristes.service`

```ini
[Unit]
Description=Lazaristes Web Application
After=network.target

[Service]
User=lazaristes
Group=lazaristes
WorkingDirectory=/home/lazaristes/lazaristes
Environment="PATH=/home/lazaristes/lazaristes/venv/bin"
Environment="WEBHOOK_SECRET=your_secret_here"
ExecStart=/home/lazaristes/lazaristes/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 4 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Activer et démarrer le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable lazaristes
sudo systemctl start lazaristes
sudo systemctl status lazaristes
```

### Étape 5 : Configuration Nginx

Créer un fichier de configuration : `/etc/nginx/sites-available/lazaristes`

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/lazaristes/lazaristes/docs/static;
    }
}
```

Activer le site :

```bash
sudo ln -s /etc/nginx/sites-available/lazaristes /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Étape 6 : Configurer SSL avec Let's Encrypt

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com
```

### Étape 7 : Configuration du webhook GitHub

Dans les paramètres GitHub de votre dépôt :
- Payload URL : `https://votre-domaine.com/webhook`
- Content type : `application/json`
- Secret : (le même que `WEBHOOK_SECRET` dans le service)

---

## Déploiement sur Heroku

### Prérequis
- Compte Heroku
- Heroku CLI installé

### Étape 1 : Préparer l'application

Créer un fichier `Procfile` :

```
web: gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
```

Créer un fichier `runtime.txt` :

```
python-3.11.0
```

### Étape 2 : Déployer sur Heroku

```bash
# Se connecter à Heroku
heroku login

# Créer une nouvelle application
heroku create lazaristes-app

# Configurer les variables d'environnement
heroku config:set WEBHOOK_SECRET=your_secret_here

# Déployer
git push heroku main

# Ouvrir l'application
heroku open
```

### Étape 3 : Configurer le webhook GitHub

URL du webhook : `https://lazaristes-app.herokuapp.com/webhook`

---

## Déploiement sur Railway

### Prérequis
- Compte Railway

### Étapes

1. **Connectez-vous à Railway** : https://railway.app

2. **Créer un nouveau projet**
   - Cliquez sur "New Project"
   - Sélectionnez "Deploy from GitHub repo"
   - Choisissez votre dépôt lazaristes

3. **Configuration automatique**
   - Railway détecte automatiquement le Dockerfile
   - Il configure le build et le déploiement

4. **Ajouter les variables d'environnement**
   - Allez dans Settings > Variables
   - Ajoutez `WEBHOOK_SECRET`

5. **Générer un domaine**
   - Allez dans Settings > Domains
   - Cliquez sur "Generate Domain"

6. **Configurer le webhook GitHub**
   - URL : `https://votre-app.railway.app/webhook`

---

## Déploiement sur DigitalOcean App Platform

### Prérequis
- Compte DigitalOcean

### Étapes

1. **Créer une nouvelle App**
   - Allez sur https://cloud.digitalocean.com/apps
   - Cliquez sur "Create App"
   - Connectez votre dépôt GitHub

2. **Configurer le build**
   - Build Command : `pip install -r requirements.txt`
   - Run Command : `gunicorn --bind 0.0.0.0:8080 --workers 2 app:app`

3. **Configurer l'environnement**
   - HTTP Port : 8080
   - Variables d'environnement : Ajoutez `WEBHOOK_SECRET`

4. **Déployer**
   - Cliquez sur "Create Resources"

5. **Configurer le webhook**
   - URL : `https://votre-app.ondigitalocean.app/webhook`

---

## Déploiement sur AWS EC2

### Prérequis
- Compte AWS
- Instance EC2 configurée

### Étape 1 : Lancer une instance EC2

```bash
# Sélectionner Ubuntu Server 22.04 LTS
# Type d'instance : t2.micro (eligible au free tier)
# Configurer le groupe de sécurité pour autoriser :
#   - SSH (port 22)
#   - HTTP (port 80)
#   - HTTPS (port 443)
```

### Étape 2 : Se connecter à l'instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### Étape 3 : Suivre les étapes du déploiement VPS

Suivez les mêmes étapes que pour le [déploiement VPS](#déploiement-sur-un-serveur-vps)

---

## GitHub Pages avec Backend

### Configuration hybride

Pour héberger le frontend sur GitHub Pages et le backend ailleurs :

#### Étape 1 : Déployer le backend

Déployez `app.py` sur n'importe quelle plateforme (Heroku, Railway, etc.)

#### Étape 2 : Modifier le frontend

Dans `docs/index.html`, modifiez la variable `API_BASE_URL` :

```javascript
const API_BASE_URL = 'https://votre-backend.herokuapp.com';
```

#### Étape 3 : Activer GitHub Pages

1. Allez dans Settings > Pages
2. Source : Deploy from a branch
3. Branch : main, folder : /docs
4. Sauvegardez

#### Étape 4 : Configurer CORS sur le backend

Le backend doit autoriser les requêtes depuis `https://matissead.github.io` :

```python
from flask_cors import CORS

CORS(app, origins=['https://matissead.github.io'])
```

---

## Mise à jour de l'application

### Sur VPS/EC2

```bash
cd /home/lazaristes/lazaristes
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart lazaristes
```

### Sur Heroku

```bash
git push heroku main
```

### Sur Railway/DigitalOcean

Ces plateformes se mettent à jour automatiquement depuis GitHub.

---

## Surveillance et maintenance

### Logs

**VPS/EC2:**
```bash
sudo journalctl -u lazaristes -f
```

**Heroku:**
```bash
heroku logs --tail
```

**Railway:**
Consultez l'onglet "Logs" dans le dashboard

### Monitoring

Considérez l'utilisation de :
- **Uptime Robot** : Surveillance de disponibilité
- **Sentry** : Suivi des erreurs
- **Prometheus + Grafana** : Métriques détaillées

### Sauvegarde

```bash
# Sauvegarder les données
tar -czf lazaristes-backup-$(date +%Y%m%d).tar.gz /home/lazaristes/lazaristes
```

---

## Résolution de problèmes courants

### Le service ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u lazaristes -n 50

# Vérifier les permissions
ls -la /home/lazaristes/lazaristes

# Tester manuellement
cd /home/lazaristes/lazaristes
source venv/bin/activate
python app.py
```

### Problèmes de webhook

- Vérifiez que le serveur est accessible depuis Internet
- Vérifiez que le secret est correctement configuré
- Consultez les logs de livraison GitHub

### Problèmes de performance

- Augmentez le nombre de workers Gunicorn
- Utilisez un cache (Redis)
- Optimisez les requêtes Git

---

## Sécurité en production

### Checklist de sécurité

- [ ] HTTPS activé (certificat SSL)
- [ ] Firewall configuré (UFW sur Ubuntu)
- [ ] Mises à jour système régulières
- [ ] Secret webhook sécurisé et complexe
- [ ] Logs de sécurité activés
- [ ] Rate limiting configuré
- [ ] CORS configuré correctement
- [ ] Variables d'environnement sécurisées (pas dans le code)

### Configuration du firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

---

## Support

Pour toute question concernant le déploiement, ouvrez une issue sur GitHub.
