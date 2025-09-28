from math import factorial
from time import sleep as s

def triangle1(n):
    for i in range(n):
        print(i*"*")

def triangle2(n):
    for i in range(n+1):
        print((n-i)*"*")


def pyramide1(n):
    triangle1(n)
    triangle2(n)


def pyramide2(n):
    for i in range(n+1):
        print((n-i)*" " + (i)*" *")


def sum(n):
    somme = 0
    for i in range(n+1):
        print(i)
        if i%3 == 0 or i%5 == 0:
            somme=somme+i
    print(str(somme))

def suite(n):
    sum2=0
    a=1
    for i in range(n+1):
        sum2=sum2 + 1/factorial(i)
    print(sum2)

def palindrome(c):
    size=len(c)
    size=size-1
    for i in range(len(c)):
        if c[i] != c[size-i]:
            print("Non")
            return False

    print("Oui")
    return True

# Exercice 16

def doublon(a):
    for i in range (len(a)):
        number_to_check=a[i]
        for k in range(len(a)):
            if number_to_check==a[k] and k != i:
                return True
    return False

# Exercice 17

def somme17(a, s):
    for i in range(len(a)):
        picked_number=a[i]
        for k in range(len(a)):
            if picked_number + a[k] == s and i != k:
                return True
    return False

