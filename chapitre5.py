# Exercice 4

def nombre_to_binaire(n):
    d = []

    while n > 0:
        d = [n % 2] + d
        n = n // 2

    return d

def espace_binaire(n):
    bin = nombre_to_binaire(n)
    cpt=0
    cpt1=0
    i=0

    for k in range(len(bin)):
        if bin[k] == 0:
            i=k
            while i < len(bin) and bin[i] != 1:
                cpt1 = cpt1 + 1
                i=i+1
            if i == len(bin):
                return cpt
            if cpt1 > cpt:
                cpt = cpt1
                cpt1 = 0
    return cpt


# Exercice 5

def factorielle(x):
    cpt=1
    for k in range(1,x+1):
        cpt=cpt*k
    return cpt

def b_to_nombre(n,b):
    nombre_b=str(n)
    nombre=0
    i=0


    for k in nombre_b:
        nombre = nombre + int(k) * (b ** (len(nombre_b)-1-i))
        i=i+1

    return [int(k) for k in str(nombre)]

def factorion(m,b):
    nb = b_to_nombre(m,b)
    somme_facto=0
    nombre=""

    for k in nb:
        nombre = nombre + str(k)

    for k in nombre:
        somme_facto = somme_facto + factorielle(int(k))

    return somme_facto == int(nombre)

def liste_factorions(b,p):
    cpt=[]

    for k in range(p+1):
        if factorion(k,b):
            cpt.append(k)
    return cpt

# Exercice 6



def decompositon(d,n):
    if d>=2**n:
        return False

    somme_bool=[]
    bin=[]

    while d > 0:
        bin = [d%2] + bin
        d = d // 2

    if len(bin) == n:
        return bin

    while len(bin) != n:
        bin = [0] + bin


    for k in range(len(bin)):
        if bin[k] == 0:
            bin[k] = False
        elif bin[k]==1:
            bin[k] = True

    return bin

def prix_decoupe(d,p):
    n = len(p) - 1
    assert len(d) == n - 1

    total = 0
    longueur = 1


    for i in range(n - 1):
        if d[i]:
            total += p[longueur]
            longueur = 1
        else:
            longueur += 1


    total += p[longueur]
    return total

def meilleur_prix(p):
    n = len(p) - 1
    best_mask = None
    best_val = -1

    for m in range(2 ** (n - 1)):
        d = decompositon(m, n - 1)
        val = prix_decoupe(d, p)
        if val > best_val:
            best_val = val
            best_mask = d

    return best_mask, best_val

# p = [0,1,5,8,9,10,17,17,20,24,26]
# best_val = 27
# best_mask = [False, False, False, False, False, True, False, True, False]






