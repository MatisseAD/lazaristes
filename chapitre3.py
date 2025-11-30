def same_elements(u,v):
    for i in range(len(u)):
        number_u=u[i]
        same_list=False
        for k in range(len(v)):
            if u[i]==v[k]:
                same_list=True
                break
        if same_list == False:
            return False
    for i in range(len(v)):
        number_v=v[i]
        same_list=False
        for k in range(len(u)):
            if v[i]==u[k]:
                same_list=True
                break
        if same_list == False:
            return False
    return True

def bien_parenthesee(s):
    parenthese_ouvrante=0
    parenthse_fermante=0
    for i in range(len(s)):
        if s[i] == '(':
            parenthese_ouvrante=parenthese_ouvrante+1
        elif s[i] == ')':
            parenthse_fermante=parenthse_fermante+1
    if parenthese_ouvrante==parenthse_fermante:
        return True
    return False


def puissance(x,n):
    if n>1:
        return x * puissance(x, n-1)
    else:
        return x

# Exercice 9
def triangle(n):
    if n == 1:
        print(n * "*")
    else:
        triangle(n-1)
        print(n*"*")

def triangle_inverse(n):
    if n == 1:
        print("*")
    else:
        print(n*"*")
        return triangle_inverse(n-1)


def sablier(n):
    if n<=0:
        return
    if n==1:
        print("*")
    else:
        print(n*"*")
        sablier(n-1)
        print(n*"*")


def subset(n):
    if not n:
        return [[]]


















