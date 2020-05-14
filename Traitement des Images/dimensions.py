import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

path = "/Users/charlotte/Desktop/Cours Mines/Informatique/Projet info 3/Traitement des Images/photos_ensembles"



from PIL import Image
import pandas as pd
#on va créer 2 séries: les hauteurs et les largeurs
def tri_bulle(liste) :
    b = True
    l = len(liste)
    while b :
        for i in range (l-1):
            if liste[i] > liste[i+1]:
                liste[i], liste[i+1] = liste[i+1], liste[i]
        for j in range(l-1) :
            if liste[i] > liste[i+1] :
                break
            b = False
    return(liste)

def dimension(chemin):
    """dossier est une liste de fichiers, importée comme définie plus tôt"""
    W = []
    H = []
    T = []
    fichiers = [f for f in listdir(chemin) if isfile(join(chemin,f))]
    for photo in fichiers:
        if photo != ".DS_Store":
            img = Image.open(chemin+"/"+photo)
            (w, h) = img.size
            W.append(w)
            H.append(h)
            T.append(w*h)
    #on veut maintenant les trier dans l'ordre croissant
    W = sorted(W)
    H = sorted(H)
    #print(W)
    return(W, H, T)


    

#on va plotter les dimensions de nos images:
W, H, T = dimension(path)
X = [i for i in range(len(W))]

plt.hist(T, bins = 20)
plt.show()

##On supprime les images extrêmes, i.e de taille entre 0 et 0,5 e7 pour plus de précision
T_bis = [t for t in T if (t <= 0.5*10**7) == True]
plt.hist(T_bis, bins = 30)
plt.show()

