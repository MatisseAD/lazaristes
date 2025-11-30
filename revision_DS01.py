def fact(n):
    if n==1:
        return n
    else:
        return n * fact(n-1)


def verif2(n):
    string=str(n)
    cpt=0
    for i in range(len(string)):
        k = int(string[i])
        cpt = cpt + fact(k)
    if cpt == n:
        return True
    return False

def solution():
    for i in range(7*fact(9)):
        if verif2(i):
            print(i)