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


def puissance(m,n):
    if n==0:
        return m
    else:
        p = n // 2
        print(m)
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







