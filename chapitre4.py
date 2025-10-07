# Exercice 1

def bicolore(t):
    l_1=[]
    l_2=[]

    cpt = 0
    i=0

    # On vérifie si la liste est strictement monotone

    for k in range(len(list)-1):
        if list[k] > list[k+1]:
            cpt = cpt + 1
    if cpt == len(list)-1:
        return True

    cpt = 0

    for k in range(len(list)-1):
        if list[k] < list[k+1]:
            cpt = cpt +1
    if cpt == len(list)-1:
        return True

    cpt = 0
    i=0

    if (len(list)) > 2:

        if list[0] > list[1]:
            while i < len(list)-1 and list[i] > list[i+1]:
                l_1.append(list[i])
                cpt = cpt +1
                i = i +1

            while i < len(list)-1 and list[i] < list[i+1]:
                l_2.append(list[i])
                cpt = cpt +1
                i = i +1

            l_2.append(list[i])

            if cpt == len(list) - 1:
                print(l_1)
                print(l_2)
                return True
            print(l_1)
            print(l_2)
            return False

        if list[0] < list[1]:
            while i < len(list)-1 and list[i] < list[i+1]:
                l_1.append(list[i])
                cpt = cpt +1
                i = i +1

            while i < len(list)-1 and list[i] > list[i+1]:
                l_2.append(list[i])
                cpt = cpt +1
                i = i + 1

            l_2.append(list[i])

            if cpt == len(list) - 1:
                print(l_1)
                print(l_2)
                return True
            print(l_1)
            print(l_2)
            return False





# Exercice 2

def entier_manquant(t):
    min=t[0]
    max=t[len(t)-1]
    list_parfaite = []

    for k in range(len(t)):
        if t[k] < min:
            min=t[k]
        if t[k] > max:
            max=t[k]

    # On construit la liste entre ces deux entiers
    for k in range(min, max+1):
        list_parfaite.append(k)

    for k in range(len(list_parfaite)):
        if list_parfaite[k] not in t:
            return list_parfaite[k]




#
# Correction
#

# Exercice 2

def contient(x,list):
    for y in list:
        if x == y:
            return True
    return False

def entier_manquant2():
    val=0
    while content(val,t):
        val=val+1
    return val

def est_croissant(t,deb,fin):
    for k in range(deb,fin-1):
        if t[k] > t[k+1]:
            return False
    return True



def est_decroissant(t,deb,fin):
    for k in range(deb,fin-1):
        if t[k] < t[k+1]:
            return False
    return True

def bicolore2(t):
    n=len(t)
    for k in range(n+1):
        if est_croissant(t,0,k) and est_decroissant(t,k,n):
            return True
        if est_decroissante(t,0,k) and est_croissant(t,k,n):
            return True
    return False

# Exercice 4

def rotation(t):
        new_list = [0] * len(t)

        for k in range(len(t)):
            if k+1 != len(t):
                new_list[k+1] = t[k]
            else:
                new_list[0] = t[k]
        return new_list



def rotation_en_place(t):
    a = rotation(t)
    for i in range(len(t)):
        t[i] = a[i]

def rotation_multiple(t,k):
    cpt=0
    while cpt != k:
        rotation_en_place(t)
        cpt = cpt +1

# Exercice 5

def swap(t,i,j):
    t[i], t[j] = t[j], t[i]

def partition(t,p):
    i = 0

    for j in range(len(t)):
        if t[j] < p:
            swap(t,j,i)
            i=i+1
    return t

def partition_hollandais(t,p):
    i,j = 0,0

    for k in range(len(t)):
        if t[k] < p:
            swap(t,k,i)
            i=i+1
        j=j+1


    for k in range(i, len(t)):
        if t[k] == p:
            swap(t,k,i)
            i=i+1
        j=j+1

def partition_hollandais_n_swap(t,p):
    i,j=0,0

    for k in range(len(t)):
        if t[k] < p:
            swap(t,k,i)
            i=i+1
            j=j+1
        elif t[k] == p:
            swap(t,k,j)
            j=j+1










