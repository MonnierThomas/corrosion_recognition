from os import listdir, makedirs
from os.path import isfile, join
from PIL import Image
from traitement_images import dimension, formatage, symetries, pre_tri, tri
from math import sqrt
import numpy as np

monchemin = ""
#répertoire où se situe mon module traitement_images
import sys
sys.path.append(monchemin)

path = ""

#on a calculé précédemment la médiane de la taille de nos images à 455 200 pixels
m = 455200

def classes_seuillees():
    """on veut ici trier nos images en 2 catégories: en-dessous et au-dessus de la médiane, et les formater à la taille moyenne de chaque sous-catégorie"""
    fichiers = [f for f in listdir(path) if isfile(join(path, f))]  
    path_petit = path + "/petites_images"
    path_grand = path + "/grandes_images"
    makedirs(path_petit)
    makedirs(path_grand)
    
    #D'abord on les trie par taille
    for photo in fichiers:
        if photo != ".DS_Store":
            image = Image.open(path + "/" + photo)
            a, b = image.size
            if a*b < m:
                image.save(path_petit+"/"+photo, quality=95)
            else:
                image.save(path_grand+"/"+photo, quality=95)
                
    #Puis on les formate
    W, H, Tp = dimension(path_petit)
    tp = np.mean(Tp)
    cp = int(sqrt(tp))    
    W, H, Tg = dimension(path_grand)
    tg = np.mean(Tg)
    cg = int(sqrt(tg))    
    path_pformat = path_petit + "/formatees"
    makedirs(path_pformat)
    path_gformat = path_grand + "/formatees"
    makedirs(path_gformat)    
    formatage((cp,cp), path_petit, path_pformat)
    formatage((cg,cg), path_grand, path_gformat)
    
    #On les symétrise pour les multiplier par 4
    symetries(path_pformat)
    symetries(path_gformat)
    
    #Ensuite on les répartit dans les dossiers train, validation et test   
    pre_tri(path_pformat)
    pre_tri(path_gformat)
    tri(path_pformat)
    tri(path_gformat)
