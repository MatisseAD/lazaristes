# Exemples de Code Python - Lazaristes

Ce document contient des exemples de code Python que vous pouvez exécuter directement dans l'interface web de Lazaristes.

## 📋 Table des matières

1. [Algorithmes de base](#algorithmes-de-base)
2. [Manipulation de listes](#manipulation-de-listes)
3. [Fonctions récursives](#fonctions-récursives)
4. [Algorithmes de tri](#algorithmes-de-tri)
5. [Mathématiques](#mathématiques)
6. [Exercices du cours](#exercices-du-cours)

---

## Algorithmes de base

### 1. Somme des multiples

Calculer la somme des multiples de 3 ou 5 jusqu'à n :

```python
def somme_multiples(n):
    total = 0
    for i in range(n + 1):
        if i % 3 == 0 or i % 5 == 0:
            total += i
    return total

result = somme_multiples(100)
print(f"Somme des multiples de 3 ou 5 jusqu'à 100 : {result}")
```

### 2. Palindrome

Vérifier si un mot est un palindrome :

```python
def est_palindrome(mot):
    mot = mot.lower()
    n = len(mot)
    for i in range(n // 2):
        if mot[i] != mot[n - 1 - i]:
            return False
    return True

mots = ["radar", "python", "kayak", "hello"]
for mot in mots:
    resultat = "est" if est_palindrome(mot) else "n'est pas"
    print(f"{mot} {resultat} un palindrome")
```

### 3. Nombre premier

Vérifier si un nombre est premier :

```python
def est_premier(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Afficher les nombres premiers jusqu'à 50
premiers = [n for n in range(2, 51) if est_premier(n)]
print(f"Nombres premiers jusqu'à 50 : {premiers}")
```

---

## Manipulation de listes

### 1. Filtrage et transformation

```python
# Liste de nombres
nombres = list(range(1, 21))

# Nombres pairs
pairs = [n for n in nombres if n % 2 == 0]
print(f"Nombres pairs : {pairs}")

# Carrés des nombres impairs
carres_impairs = [n**2 for n in nombres if n % 2 != 0]
print(f"Carrés des impairs : {carres_impairs}")

# Somme des cubes
somme_cubes = sum(n**3 for n in nombres)
print(f"Somme des cubes : {somme_cubes}")
```

### 2. Recherche dans une liste

```python
def trouve_paire_somme(liste, cible):
    """Trouve deux nombres dont la somme est égale à la cible"""
    for i in range(len(liste)):
        for j in range(i + 1, len(liste)):
            if liste[i] + liste[j] == cible:
                return (liste[i], liste[j])
    return None

nombres = [2, 7, 11, 15, 3, 6]
cible = 9
paire = trouve_paire_somme(nombres, cible)
if paire:
    print(f"Paire trouvée : {paire[0]} + {paire[1]} = {cible}")
else:
    print("Aucune paire trouvée")
```

### 3. Manipulation avancée

```python
# Liste d'altitudes (comme dans TP02)
altitudes = [0, 300, 500, 600, 1000, 800, 900, 500, 600, 200, 0]

# Altitude maximale
alt_max = max(altitudes)
print(f"Altitude maximale : {alt_max}m")

# Dénivelés positifs
deniveles = []
for i in range(1, len(altitudes)):
    deniv = altitudes[i] - altitudes[i-1]
    if deniv > 0:
        deniveles.append(deniv)
print(f"Dénivelés positifs : {deniveles}")
print(f"Dénivelé positif total : {sum(deniveles)}m")
```

---

## Fonctions récursives

### 1. Factorielle

```python
def factorielle(n):
    if n <= 1:
        return 1
    return n * factorielle(n - 1)

# Calculer factorielles de 0 à 10
for i in range(11):
    print(f"{i}! = {factorielle(i)}")
```

### 2. Suite de Fibonacci

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Afficher les 15 premiers termes
print("Suite de Fibonacci :")
fibs = [fibonacci(i) for i in range(15)]
print(fibs)
```

### 3. Somme des chiffres

```python
def somme_chiffres(n):
    if n < 10:
        return n
    return (n % 10) + somme_chiffres(n // 10)

nombres = [123, 456, 789, 1234]
for n in nombres:
    print(f"Somme des chiffres de {n} : {somme_chiffres(n)}")
```

---

## Algorithmes de tri

### 1. Tri à bulles

```python
def tri_bulles(liste):
    n = len(liste)
    for i in range(n):
        for j in range(0, n - i - 1):
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
    return liste

nombres = [64, 34, 25, 12, 22, 11, 90]
print(f"Liste originale : {nombres}")
tri_bulles(nombres)
print(f"Liste triée : {nombres}")
```

### 2. Tri par sélection

```python
def tri_selection(liste):
    n = len(liste)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if liste[j] < liste[min_idx]:
                min_idx = j
        liste[i], liste[min_idx] = liste[min_idx], liste[i]
    return liste

nombres = [64, 25, 12, 22, 11]
print(f"Avant tri : {nombres}")
tri_selection(nombres)
print(f"Après tri : {nombres}")
```

### 3. Tri par insertion

```python
def tri_insertion(liste):
    for i in range(1, len(liste)):
        cle = liste[i]
        j = i - 1
        while j >= 0 and liste[j] > cle:
            liste[j + 1] = liste[j]
            j -= 1
        liste[j + 1] = cle
    return liste

nombres = [12, 11, 13, 5, 6]
print(f"Non trié : {nombres}")
tri_insertion(nombres)
print(f"Trié : {nombres}")
```

---

## Mathématiques

### 1. PGCD (Plus Grand Commun Diviseur)

```python
def pgcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def ppcm(a, b):
    return abs(a * b) // pgcd(a, b)

print(f"PGCD(48, 18) = {pgcd(48, 18)}")
print(f"PPCM(48, 18) = {ppcm(48, 18)}")
```

### 2. Nombres parfaits

```python
def est_parfait(n):
    diviseurs = [i for i in range(1, n) if n % i == 0]
    return sum(diviseurs) == n

# Trouver les nombres parfaits jusqu'à 1000
parfaits = [n for n in range(2, 1001) if est_parfait(n)]
print(f"Nombres parfaits jusqu'à 1000 : {parfaits}")
```

### 3. Triangle de Pascal

```python
def pascal(n):
    """Génère les n premières lignes du triangle de Pascal"""
    triangle = []
    for i in range(n):
        ligne = [1]
        if i > 0:
            for j in range(len(triangle[i-1]) - 1):
                ligne.append(triangle[i-1][j] + triangle[i-1][j+1])
            ligne.append(1)
        triangle.append(ligne)
    return triangle

# Afficher 8 lignes
triangle = pascal(8)
for ligne in triangle:
    print(ligne)
```

---

## Exercices du cours

### 1. Pyramide d'étoiles

```python
def pyramide(n):
    """Affiche une pyramide de n lignes"""
    for i in range(1, n + 1):
        espaces = " " * (n - i)
        etoiles = "*" * (2 * i - 1)
        print(espaces + etoiles)

pyramide(5)
```

### 2. Fonction bicolore

Vérifier si une liste est monotone par morceaux :

```python
def est_croissant(liste, debut, fin):
    for i in range(debut, fin - 1):
        if liste[i] >= liste[i + 1]:
            return False
    return True

def est_decroissant(liste, debut, fin):
    for i in range(debut, fin - 1):
        if liste[i] <= liste[i + 1]:
            return False
    return True

def bicolore(liste):
    n = len(liste)
    # Test si strictement croissant ou décroissant
    if est_croissant(liste, 0, n) or est_decroissant(liste, 0, n):
        return True
    
    # Test décroissant puis croissant
    for k in range(n + 1):
        if est_decroissant(liste, 0, k) and est_croissant(liste, k, n):
            return True
        if est_croissant(liste, 0, k) and est_decroissant(liste, k, n):
            return True
    return False

# Tests
print(f"[1,2,3,4] : {bicolore([1,2,3,4])}")
print(f"[5,4,3,2,1] : {bicolore([5,4,3,2,1])}")
print(f"[5,4,1,2,3] : {bicolore([5,4,1,2,3])}")
print(f"[1,4,2,3] : {bicolore([1,4,2,3])}")
```

### 3. Rotation de liste

```python
def rotation(liste):
    """Effectue une rotation vers la droite"""
    if len(liste) <= 1:
        return liste
    nouvelle = [0] * len(liste)
    nouvelle[0] = liste[-1]
    for i in range(len(liste) - 1):
        nouvelle[i + 1] = liste[i]
    return nouvelle

liste_origine = [1, 2, 3, 4, 5]
print(f"Liste originale : {liste_origine}")
for i in range(3):
    liste_origine = rotation(liste_origine)
    print(f"Après rotation {i+1} : {liste_origine}")
```

---

## Conseils d'utilisation

### Limites de l'environnement

L'environnement d'exécution a les restrictions suivantes :

✅ **Autorisé :**
- Fonctions built-in de base (print, len, range, etc.)
- Structures de contrôle (if, for, while)
- Définition de fonctions
- List comprehensions
- Opérations mathématiques

❌ **Non autorisé :**
- Imports de modules (import os, import sys, etc.)
- Accès aux fichiers (open, read, write)
- Fonctions d'exécution dynamique (eval, exec)
- Variables globales du système

### Astuces

1. **Utilisez print() abondamment** pour déboguer votre code
2. **Testez avec des petits exemples** avant de passer à des cas complexes
3. **Vérifiez les cas limites** (listes vides, nombres négatifs, etc.)
4. **Utilisez des fonctions** pour organiser votre code
5. **Commentez votre code** pour mieux le comprendre

### Exercices suggérés

1. Modifiez les exemples ci-dessus
2. Combinez plusieurs algorithmes
3. Optimisez les solutions proposées
4. Créez vos propres variations

---

## 🎯 Défis

### Défi 1 : Suite de Syracuse
Implémenter la conjecture de Syracuse (ou suite de Collatz)

### Défi 2 : Anagrammes
Trouver si deux mots sont des anagrammes

### Défi 3 : Nombre d'Armstrong
Vérifier si un nombre est un nombre d'Armstrong

### Défi 4 : Plus longue sous-séquence croissante
Trouver la plus longue sous-séquence strictement croissante

---

**Bon codage ! 🐍**

Pour plus d'exemples et d'exercices, consultez les notebooks explicatifs dans le dépôt.
