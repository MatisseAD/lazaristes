# Guide de Sécurité - Lazaristes

Ce document décrit les considérations de sécurité pour l'application Lazaristes et fournit des recommandations pour un déploiement sécurisé.

## Table des matières

1. [Sandboxing du code Python](#sandboxing-du-code-python)
2. [Limitation de taux](#limitation-de-taux)
3. [Validation des webhooks](#validation-des-webhooks)
4. [Protection contre les attaques](#protection-contre-les-attaques)
5. [Bonnes pratiques](#bonnes-pratiques)
6. [Signalement de vulnérabilités](#signalement-de-vulnérabilités)

---

## Sandboxing du code Python

### Mécanisme de sécurité

L'application utilise plusieurs niveaux de protection pour l'exécution de code Python :

#### 1. Environnement restreint (`restricted_globals`)

Seules les fonctions built-in sûres sont disponibles :

**Fonctions autorisées :**
- Affichage : `print`
- Types de base : `str`, `int`, `float`, `bool`
- Structures de données : `list`, `dict`, `tuple`, `set`
- Fonctions mathématiques : `abs`, `max`, `min`, `sum`, `pow`, `round`
- Fonctions d'itération : `len`, `range`, `sorted`, `reversed`, `enumerate`, `zip`, `map`, `filter`, `any`, `all`

**Fonctions/modules interdits :**
- ❌ `import` (aucun import de module)
- ❌ `open`, `file` (pas d'accès aux fichiers)
- ❌ `eval`, `exec`, `compile` (pas d'exécution dynamique supplémentaire)
- ❌ `__import__` (pas d'import dynamique)
- ❌ Modules système (`os`, `sys`, `subprocess`)
- ❌ Modules réseau (`socket`, `requests`, `urllib`)

#### 2. Limitations de ressources

```python
# Limite de taille du code
MAX_CODE_LENGTH = 10000  # caractères

# Limite de temps d'exécution
# Note : Nécessite une implémentation plus robuste en production
```

#### 3. Isolation de la sortie

La sortie standard et la sortie d'erreur sont capturées et isolées :

```python
redirected_output = StringIO()
redirected_error = StringIO()
sys.stdout = redirected_output
sys.stderr = redirected_error
```

### Limitations connues

⚠️ **Attention** : Le sandboxing actuel a des limitations :

1. **Pas de timeout strict** : Le code peut potentiellement s'exécuter indéfiniment
2. **Consommation mémoire** : Pas de limite stricte sur l'utilisation de la mémoire
3. **Boucles infinies** : Possibles mais limitées par le timeout du serveur web

### Recommandations pour un sandboxing renforcé

Pour un environnement de production robuste, considérez :

#### Option 1 : RestrictedPython

```python
from RestrictedPython import compile_restricted, safe_globals

# Compiler le code de manière sécurisée
byte_code = compile_restricted(code, '<string>', 'exec')
exec(byte_code, safe_globals)
```

#### Option 2 : Conteneurs Docker isolés

Exécuter chaque requête dans un conteneur Docker jetable :

```python
import docker

client = docker.from_env()
result = client.containers.run(
    'python:3.11-alpine',
    f'python -c "{code}"',
    remove=True,
    mem_limit='50m',
    network_disabled=True,
    timeout=5
)
```

#### Option 3 : Services de sandboxing externes

Utiliser des services comme :
- **Judge0** : API de sandboxing de code
- **Piston** : Moteur d'exécution de code isolé
- **CodeSandbox** : Environnement d'exécution sécurisé

---

## Limitation de taux

### Mécanisme actuel

L'application implémente une limitation de taux basique :

```python
RATE_LIMIT_WINDOW = 60  # secondes
RATE_LIMIT_MAX_REQUESTS = 10  # requêtes par fenêtre
```

**Limites :**
- 10 requêtes par minute par adresse IP
- Stockage en mémoire (perdu au redémarrage)

### Code de limitation

```python
@rate_limit
def execute_code():
    # Protection contre les abus
    ...
```

### Amélioration recommandée

Pour une limitation de taux plus robuste en production :

#### Option 1 : Redis

```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def rate_limit_redis(limit=10, window=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            key = f'rate_limit:{client_ip}'
            
            current = redis_client.get(key)
            if current and int(current) >= limit:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, window)
            pipe.execute()
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

#### Option 2 : Flask-Limiter

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/execute', methods=['POST'])
@limiter.limit("10 per minute")
def execute_code():
    ...
```

---

## Validation des webhooks

### Validation HMAC

L'application valide les webhooks GitHub en utilisant HMAC-SHA256 :

```python
expected_signature = 'sha256=' + hmac.new(
    WEBHOOK_SECRET.encode(),
    request.data,
    hashlib.sha256
).hexdigest()

if not hmac.compare_digest(signature, expected_signature):
    return jsonify({'error': 'Invalid signature'}), 401
```

### Configuration du secret

⚠️ **Important** : Utilisez un secret fort :

```bash
# Générer un secret sécurisé
python -c "import secrets; print(secrets.token_hex(32))"
```

### Validation des événements

Filtrez les événements webhook selon vos besoins :

```python
event = request.headers.get('X-GitHub-Event', 'unknown')

# Accepter uniquement les événements push
if event != 'push':
    return jsonify({'message': 'Event ignored'}), 200
```

---

## Protection contre les attaques

### 1. Cross-Site Scripting (XSS)

**Protection implémentée :**

Frontend JavaScript :
```javascript
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
```

Toutes les sorties utilisateur sont échappées avant affichage.

### 2. Injection de code

**Protection implémentée :**
- Pas d'utilisation de `eval()` en JavaScript
- Pas d'injection SQL (pas de base de données)
- Validation des entrées côté serveur

### 3. Cross-Origin Resource Sharing (CORS)

**Configuration actuelle :**
```python
from flask_cors import CORS
CORS(app)  # Permet toutes les origines
```

**Configuration recommandée en production :**
```python
CORS(app, origins=[
    'https://votre-domaine.com',
    'https://matissead.github.io'
])
```

### 4. Déni de service (DoS)

**Protections :**
- Limitation de taux
- Limite de taille du code (10 000 caractères)
- Timeout des requêtes (configurable dans Gunicorn)

**Recommandations supplémentaires :**
- Utiliser un CDN (Cloudflare)
- Configurer un reverse proxy avec limitation
- Utiliser un WAF (Web Application Firewall)

### 5. Man-in-the-Middle (MITM)

**Protection :**
- ✅ Utiliser HTTPS en production
- ✅ Configurer HSTS (HTTP Strict Transport Security)

Configuration Nginx :
```nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
```

---

## Bonnes pratiques

### 1. Variables d'environnement

❌ **À éviter :**
```python
WEBHOOK_SECRET = "mon_secret_123"  # Jamais en dur !
```

✅ **Bonne pratique :**
```python
WEBHOOK_SECRET = os.environ.get('WEBHOOK_SECRET', '')
```

### 2. Gestion des erreurs

Ne pas exposer les détails techniques dans les messages d'erreur :

```python
try:
    # Code sensible
    ...
except Exception as e:
    # Ne pas exposer e directement
    return jsonify({'error': 'Internal server error'}), 500
```

### 3. Logging

Loguer les activités suspectes :

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Loguer les tentatives d'abus
if len(code) > MAX_CODE_LENGTH:
    logger.warning(f'Code too long from IP {request.remote_addr}')
```

### 4. Mises à jour

Maintenir les dépendances à jour :

```bash
# Vérifier les vulnérabilités
pip install safety
safety check

# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt
```

### 5. Headers de sécurité

Ajouter des headers de sécurité :

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

---

## Checklist de sécurité pour la production

- [ ] HTTPS activé avec certificat SSL valide
- [ ] Secret webhook fort et unique
- [ ] Variables d'environnement sécurisées (pas dans le code)
- [ ] CORS configuré avec origines spécifiques
- [ ] Rate limiting configuré
- [ ] Logging des activités activé
- [ ] Firewall configuré (UFW, iptables)
- [ ] Mises à jour système régulières
- [ ] Sauvegarde régulière des données
- [ ] Monitoring et alertes configurés
- [ ] Headers de sécurité ajoutés
- [ ] Sandboxing renforcé (Docker ou RestrictedPython)
- [ ] Timeout d'exécution strict
- [ ] Limite de ressources (CPU, mémoire)

---

## Tests de sécurité

### Test de sandboxing

Tentez d'exécuter du code malveillant (dans un environnement de test) :

```python
# Ces tests doivent échouer :

# Tentative d'import
import os
os.system('ls')

# Tentative d'accès aux fichiers
open('/etc/passwd', 'r').read()

# Tentative d'exécution de code
eval('1+1')
```

### Test de limitation de taux

```bash
# Envoyer plus de 10 requêtes en une minute
for i in {1..15}; do
  curl -X POST http://localhost:5000/api/execute \
    -H "Content-Type: application/json" \
    -d '{"code": "print(\"test\")"}'
done
```

### Test de webhook

```bash
# Sans signature (doit échouer)
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Avec mauvaise signature (doit échouer)
curl -X POST http://localhost:5000/webhook \
  -H "X-Hub-Signature-256: sha256=invalid" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

---

## Signalement de vulnérabilités

Si vous découvrez une vulnérabilité de sécurité, veuillez :

1. **Ne pas** la divulguer publiquement
2. Ouvrir une issue GitHub privée ou contacter les mainteneurs
3. Fournir un maximum de détails :
   - Nature de la vulnérabilité
   - Étapes pour la reproduire
   - Impact potentiel
   - Suggestions de correction (si possible)

---

## Ressources supplémentaires

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [GitHub Webhook Security](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks)

---

**Note** : La sécurité est un processus continu. Restez informé des nouvelles vulnérabilités et mettez à jour régulièrement vos dépendances et votre configuration.
