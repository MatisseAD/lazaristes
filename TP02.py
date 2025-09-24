alt = [0,300,500,600,1000,800,900,500,600,200,0]

def altmax(list):
    alt_max=0
    for i in range(len(list)):
        if list[i] > alt_max:
            alt_max=list[i]
    return alt_max

def deniv_max(list):
    den_max=0
    for i in range(1, len(list)):
        if abs(list[i] - list[i-1]) > den_max:
            den_max=list[i]-list[i-1]
    return den_max

def heure_deniv_max(list):
    for i in range(1, len(list)):
        if abs(list[i] - list[i-1]) == deniv_max(list):
            return i-1
    return None

def deniv_positif_total(list):
    tot=0
    for i in range(1,len(list)):
        if list[i-1] < list[i] and i < len(list):
            tot=tot+(list[i]-list[i-1])
    return tot

def sommets(list):
    for i in range(1,len(list)):
        if i+1 < len(list):
            if list[i] > list[i-1] and list[i] > list[i+1]:
                print(list[i])



def altitudecaca(list):
    altitude=0
    for k in range(len(list)):
        if list[k] > altitude:
            altitude=list[k]
    return altitude

print(str(altitudecaca(alt)))
