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








