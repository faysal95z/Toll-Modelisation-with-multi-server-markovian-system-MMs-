import numpy as np
import matplotlib.pyplot as plt
import random as rd

#Modèle M/M/s dans le cas d'une HISTORY de péage sans distinction de véhicules :

#Définission des paramètres de la modélisation par l'utilisateur
try :
    T = int(input("Durée de l'expérience en minutes ? T = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}")


try :
    st = int(input("Combien de sortie télépéage ? st = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}")
try :
    sc = int(input("Combien de sortie carte bancaire ? sc = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}")
try :
    sl = int(input("Combien de sortie liquide ? sl = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}")

pt,pc,pl = (0,0,0)
while pt+pc+pl < .99999 or pt+pc+pl > 1.0 :
    try :
        pt = float(input("Proportion d'utilisateurs télépéage ? pt = "))
    except ValueError :
        print(f"Une erreur est survenue : {ValueError}")
    try :
        pc = float(input("Proportion d'utilisateurs carte bancaire ? pc = "))
    except ValueError :
        print(f"Une erreur est survenue : {ValueError}")
    try :
        pl = float(input("Proportion d'utilisateurs liquide ? pl = "))
    except ValueError :
        print(f"Une erreur est survenue : {ValueError}")


try :
    lambdA = int(input("Valeur du paramètre lambda = nbVehicule/minute. lambda = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}")

try :
    muT = 1/float(input("Valeur du paramètre 1/muT = tempsTraitementMoyenTelepeage. 1/muT = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}")

try :
    muC = 1/float(input("Valeur du paramètre 1/muC = tempsTraitementMoyenCB. 1/muC = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}") 

try :
    muL = 1/float(input("Valeur du paramètre 1/muL = tempsTraitementMoyenLiquide. 1/muL = "))
except ValueError :
    print(f"Une erreur est survenue : {ValueError}") 


# Implémentation de la fonction de répartition de la variable aléatoire suivant une loi exponentielle négative de paramètre mu
def fRepTA(t,mu) -> float :
    return 1-np.exp(-mu*t)

# Fonction Temps d'Attente. Réalise une expérience aléatoire : tire un "réel" dans [0;1], et le place dans [0 ; F(1dt)[ U [F(1dt) ; F(2dt)[ U ... U [F(10dt) ; F(11dt)[ U [F(11dt) ; 1]
def TA(mu) -> int :
    x = rd.random()
    if 0 <= x < fRepTA(1/lambdA, mu) :
        return 1
    elif fRepTA(1/lambdA, mu) <= x < fRepTA(2/lambdA, mu) :
        return 2
    elif fRepTA(2/lambdA, mu) <= x < fRepTA(3/lambdA, mu) :
        return 3
    elif fRepTA(3/lambdA, mu) <= x < fRepTA(4/lambdA, mu) :
        return 4
    elif fRepTA(4/lambdA, mu) <= x < fRepTA(5/lambdA, mu) :
        return 5
    elif fRepTA(5/lambdA, mu) <= x < fRepTA(6/lambdA, mu) :
        return 6
    elif fRepTA(6/lambdA, mu) <= x < fRepTA(7/lambdA, mu) :
        return 7
    elif fRepTA(7/lambdA, mu) <= x < fRepTA(8/lambdA, mu) :
        return 8
    elif fRepTA(8/lambdA, mu) <= x < fRepTA(9/lambdA, mu) :
        return 9
    elif fRepTA(9/lambdA, mu) <= x < fRepTA(10/lambdA, mu) :
        return 10
    elif fRepTA(10/lambdA, mu) <= x < fRepTA(11/lambdA, mu) :
        return 11
    elif fRepTA(11/lambdA, mu) <= x :
        return 12

# Définition de la gare de péage

# guich = [nbDeVoitures, "typeDeGuichet", tempsDeTraitement, dateArriveeAuGuichet]
# GARE = {0 : guichet0, 1 : guichet 2, ... , N-1 : guichetN} HISTORY = [gareT0, gareT1, ...]

GUIinnit = {}
for k in range(st):
    GUIinnit[k] = [0,"t",TA(muT),0]
for k in range(st+sc)[st:] :
    GUIinnit[k] = [0,"c",TA(muC),0]
for k in range(st+sc+sl)[st+sc:] :
    GUIinnit[k] = [0,"l",TA(muL),0]

# Enregistrement de l'état de la gare à 0dt
HISTORY = [GUIinnit]

# Classico classique
def facto(n) -> int :
    if n == 0 :
        return 1
    return facto(n-1)

# Fonction d'apparition, lorsqu'un véhicule apparait elle indique le type de véhicule pour l'acheminer vers le type de guichet qui lui correspond.
def apparaitSur() -> str :
    x = rd.random()
    if 0 <= x < pt :
        return "t"
    elif pt <= x < pt + pc :
        return "c"
    else :
        return "l"

# Calcul la probabilité qu'une variable aléatoire suivant une loi de poission de paramètre 1 ait une valeur de 0, 1, 2, 3 ou 4 et l'enregistre dans la liste Pdt
# Pdt(n) = exp(-1)/n!
# FrepP(n) = {\sigma}_{k=0}^n Pdt(n)
Pdt = [np.exp(-1)]
FrepP = [np.exp(-1)]
for n in range(5)[1:]:
    Pdt.append(np.exp(-1)/facto(n))
    FrepP.append(FrepP[n-1]+Pdt[n])

# Fonction Nombre d'apparition entre t et t+dt. Réalise une expérience aléatoire : tire un "réel" dans [0;1] puis le place dans [0 ; FrepP[0][ U [FrepP[0] ; FrepP[1][ U ... U [FrepP[3] ; FrepP[4][ U [Frep[4] ; 1]
def NbDt() -> int :
    x = rd.random()
    if 0 <= x < FrepP[0] :
        return 0
    elif FrepP[0] <= x < FrepP[1] :
        return 1
    elif FrepP[1] <= x < FrepP[2] :
        return 2
    elif FrepP[2] <= x < FrepP[3] :
        return 3
    elif FrepP[3] <= x < FrepP[4] :
        return 4
    elif FrepP[4] <= x <= 1 :
        return 5

# Donne le nombre de véhicule d'un type à chaque instant
def NbActuelVeh(typeGuichet,t) -> int :
    if typeGuichet == "t" :
        N = 0
        for k in range(st):
            N += HISTORY[t][k][0]
        return N
    if typeGuichet == "c" :
        N = 0
        for k in range(sc):
            N += HISTORY[t][st+k][0]
        return N
    if typeGuichet == "t" :
        N = 0
        for k in range(sl):
            N += HISTORY[t][st+sc+k][0]
        return N

# Sors l'indice du guichet contenant le moins de véhicule en attente (etat contient le nombre de véhicules en attente pour un même type de guichet, dans l'ordre)
def NumGuichetEntr(etat) -> int :
    m = etat[0]
    i = 0
    for n in range(len(etat)) :
        if etat[n] <= m :
            i = n
            m = etat[n]
    return i

# Donne l'indice du guichet à traiter
def indiceGuichTraiter(typeVeh,hist,t) -> int :
    etatGuichmmType = []
    if typeVeh == "t" :
            for k in range(st):
                etatGuichmmType.append(hist[t-1][k][0])
            numGuich = NumGuichetEntr(etatGuichmmType)
    elif typeVeh == "c" :
            for k in range(st+sc)[st:]:
                etatGuichmmType.append(hist[t-1][k][0])
            numGuich = NumGuichetEntr(etatGuichmmType) + st
    elif typeVeh == "l" :
            for k in range(st+sc+sl)[st+sc:]:
                etatGuichmmType.append(hist[t-1][k][0])
            numGuich = NumGuichetEntr(etatGuichmmType) + st + sc
    return numGuich

# Fait passer un véhicule ou non sur un guichet donné
def traiter(guich,t) :
    if guich[0] > 0 :
        if guich[2] + guich[3] == t :
            guich[0] += -1
            guich[3] = t
            if guich[1] == "t" :
                guich[2] = TA(muT)
            elif guich[1] == "c" :
                guich[2] = TA(muC)
            elif guich[1] == "l" :
                guich[2] = TA(muL)
    return

# Expérience sur une durée de T dt
for t in range(T)[1:] :
    HISTORY.append({})
    aTraiter = {}
    for k in range(st+sc+sl):
        aTraiter[k] = k
    NbApparu = NbDt()
    for n in range(NbApparu) :
        typeVehicule = apparaitSur()
        i = indiceGuichTraiter(typeVehicule,HISTORY,t)
        Nguichet = [HISTORY[t-1][i][0]+1, HISTORY[t-1][i][1], HISTORY[t-1][i][2], HISTORY[t-1][i][3]]
        traiter(Nguichet,t)
        HISTORY[t][i] = Nguichet
        if i in aTraiter :
            aTraiter.pop(i)
    for i in aTraiter :
        Nguichet = [HISTORY[t-1][i][0], HISTORY[t-1][i][1], HISTORY[t-1][i][2], HISTORY[t-1][i][3]]
        HISTORY[t][i] = Nguichet

print(len(HISTORY))

print(HISTORY[0])
print(HISTORY[14])
print(HISTORY[29])
print(HISTORY[44])
print(HISTORY[59])

print(HISTORY)

def dispGuichet(i,ty):
    if ty == "t" :
        col = "orange"
    elif ty == "c" :
        col = "green"
    elif ty == "l" :
        col = "blue"
    guichetBottom = [[0,0],[6*i,6*i+2]]
    guichetTop = [[0,0],[6*i+4,6*i+6]]
    plt.plot(guichetBottom[0],guichetBottom[1],color=col,linewidth=2)
    plt.plot(guichetTop[0],guichetTop[1],color=col,linewidth=2)
    return

def dispGare(hist,t,i) :
    n = hist[t][i][0]
    x = []
    y = []
    for k in range(n):
        x.append(4*k)
        y.append(6*i+3)
    plt.scatter(x,y,marker="o",s=8,c="red")
    return

tAffiche = [0,T//3,2*T//3,T-1]

for t in tAffiche:
    for k in range(st+sc+sl):
        dispGuichet(k,HISTORY[t][k][1])
        dispGare(HISTORY,t,k)
    plt.axis("equal")
    plt.title(f"Etat de la gare à l'instant {t}dt = {60*t/lambdA}s, pour {st} sorties telepeage, {sc} sorties CB, {sl} sorties espèce avec {lambdA} vehicules par minutes, {100*pt} Telepeage, {100*pc} CB et {100*pl} espèce.\nTemps de traitement moyen : 1/muT = {60/muT}s, 1/muC = {60/muC}, 1/muL = {60/muL}")
    plt.show()


Xflux = range(T)
Yflux = []
for G in HISTORY :
    print(G)
    n = 0
    for k in range(st+sc+sl) :
        n += G[k][0]
    n = n/(st+sc+sl)
    Yflux.append(n)

plt.plot(Xflux,Yflux)
plt.title(f"Nb moyen de vehicules par guichets en fonction du temps (en dt = {60/lambdA}s)")

plt.show()
