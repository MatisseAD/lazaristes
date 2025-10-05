# Cryptage de César

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def ordre(c):
    return ord(c) - 97

def lettre(n):
    if n < 0 or n > 25:
        return "null"

    for k in alphabet:
        if ordre(k) == n:
            return k

def est_lettre_alphabet(c):
    for k in alphabet:
        if c == k:
            return True
    return False

def code(m,c):
    encoded_message=''

    for k in m:

        a = ordre(k) + ordre(c)

        if a > 25:
            a=a-25

        lettre_encode = lettre(a)

        encoded_message = encoded_message + lettre_encode

    return encoded_message

def decode(m,c):
    decoded_message=''

    for k in m:

        a = ordre(k) - ordre(c)

        if a < 0:
            a = a+25

        lettre_dedcode=lettre(a)

        decoded_message = decoded_message + lettre(a)

    return decoded_message