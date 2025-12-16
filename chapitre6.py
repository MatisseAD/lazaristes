import time

# Exercice 2

def delta(t,k):
    cpt1=0
    cpt2=0
    for i in range(k):
        cpt1=cpt1 + t[i]
    for i in range(k, len(t)):
        cpt2=cpt2 + t[i]
    return cpt1 - cpt2

# Complexité delta -> O(2n) = O(n)

def equilibre(t):
    min=max(t)

    for k in range(lent(t)):
        if delta(t,k)<min:
            min=delta(t,k)
    return min

# Complexité equilibre O(n²)


# Complexité quasi-linéaire


# Exercice 4

def cherche_somme(t,s):
    for i in range(len(t)):
        for j in range(len(t)):
            if t[i] + t[j] == s and i != j:
                return (i,j)

# Complexité O(n²)

def cherche_somme_croissant(t,s):
    cpt=0
    i=0
    j=len(t)-1
    for k in range(len(t)):
        cpt = t[i] + t[j]
        if cpt < s:
            i = i +1
        elif cpt > s:
            j=j-1
        elif cpt == s:
            return (i,j)
    return None

# Complexité O(n)

# Tri fusion

def tri_fusion(t):
    n=len(t)
    if n <= 1:
        return t[:]
    else:
        n1=n//2
        t1=tri_fusion(t[0:n1])
        t2=tri_fusion(t[n1:n])
        t=fusion(t1,t2)
        return t

def fusion(t1,t2):
    t = []
    i=0
    j=0

    while i < len(t1) and j < len(t2):
        if t1[i] <= t2[j]:
            t.append(t1[i])
            i=i+1
        else:
            t.append(t2[j])
            j=j+1

    t.extend(t1[i:])
    t.extend(t2[j:])
    return t



def cherche_somme_lin(t,s):
    return cherche_somme_croissant(tri_fusion(t), s)




# Exercice 7

tibo = [
    [1,2,3],
    [4,5,6],
    [7,8,9]
]

mat = [
    [1,2,3],
    [7,8,9],
    [4,5,6]
]

def produit(a, b):
    len_matrix = len(a)
    m_out = [[0 for _ in range(len_matrix)] for _ in range(len_matrix)]

    for i in range(len_matrix):
        for j in range(len_matrix):
            cpt = 0
            for k in range(len_matrix):
                cpt += a[i][k] * b[k][j]
            m_out[i][j] = cpt
    return m_out

# Complexité Theta(log(n) * n3)

def puissance(m,n):
    if n==0:
        ans = [[0 for _ in range(len(m))] for _ in range(len(m))]
        return
    else:
        p = n // 2
        y = puissance(m,p)
        if n % 2 == 0:
            return produit(y,y)
        else:
            return produit(m, produit(y,y))


# Fibo complexité Thêta(log(n))

def fibo(n):
    m_fibo = [[1,1], [1,0]]
    m_fibo_n = puissance(m_fibo, n)
    return m_fibo_n[0][0] + m_fibo_n[1][0]

# Exercice 16

def suite(n):
    if n == 0:
     return 1.0
    else:
        s = 0.0
        for k in range(1, n + 1):
            s = s + suite(n - k) / k
        return s

suite(4)


def memo(n):
    memo = [0 for _ in range(n+1)]
    memo[0] = 1

    for k in range(1,n+1):
        cpt=0
        for i in range(k):
            cpt = memo[i]/(k-i) + cpt
        memo[k] = cpt


    return memo[n]


# Exercice 7 tri par insertion dichotomique
# Soit n, la taille de la liste t

def indice(t,k):
    val = t[k]
    a, b = 0, k
    while a < b:
        m = (a + b) // 2
        if t[m] < val:
            a = m + 1
        else:
            b = m
    return a

# Complexité de comparaison : O(log(k))
# Complexité d'affectation : O(log(k))

def swap(t,i,j):
    t[i],t[j]=t[j],t[i]

# Complexité d'affectation : O(1)

def insertion(t,k):
    i=indice(t,k)

    for l in range(i, len(t)):
        swap(t,l,len(t)-1)

# On fait environ k appel à swap donc k affection : O(k)
# Complexité d'affectation : O(log(k) + k) = O(k)


def tri_insertion(t):
    for i in range(1,len(t)):
        insertion(t,i)

# On fait n appel à insertion
# (COMPLEXITE D'AFFECTATION) Donc,  TRI_INSERTION : C(n) = O(n²)

# Complexité du nombre de comparaison : O(n*log(n)) (PAS CONFONDRE AVEC COMPLEXITE TEMPORELLE)
# (seul la fonction indice() effectue une comparaison)


def grenouille(m,t):
    bool_caillou = [False for _ in range(m)]
    perfect = [True for _ in range(m)]

    for i in range(len(t)):
        bool_caillou[t[i]] = True
        if bool_caillou == perfect:
            return i

# Complexité temporelle : O(2n) = O(n)
# Complexité spatiale : O(2m) = O(m)

# Correction grenouille

def appartient(t,k):
    for x in t:
        if x==k:
            return True
    return False

def grenouille_correction(m,t):
    lp=[]
    i=0
    cpt=0
    n=len(t)
    while cpt != m and i < n:
        if not appartient(lp, t[i]):
            cpt += 1
            lp.append(t[i])
        i += 1
    return i-1

def grenouille_corr_2(m,t):
    cpt = 0
    r = [False for _ in range(m)]
    for i in range(len(t)):
        if not r[t[i]]:
            r[t[i]] = True
            cpt += 1
        if cpt == m:
            return i
            
# Complexité en O(n) temporel et algo spatial en theta m


















