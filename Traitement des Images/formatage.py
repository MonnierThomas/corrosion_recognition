path1 = 'path1'
path2 = 'path2'

from os import listdir
from os.path import isfile, join

from PIL import Image
import pandas as pd


def dimensionnement(image, W, H, nv_nom):
    img = Image.open(image)
    image = img.resize((W, H), Image.ANTIALIAS)
    image.save(nv_nom, quality=95)



def formatage(path1, path2):
    """path1 est le chemin vers le dossier regroupant les photos originales, path2 le chemin d'arrivée"""
    
    #on commence par chercher les tailles finales de nos images
    fichiers = [f for f in listdir(path1) if isfile(join(path1, f))]
    print(fichiers)
    W = []
    H = []
    
    for photo in fichiers:
        img = Image.open(path1 + photo)
        (w, h) = img.size
        W.append(w)
        H.append(h)
        
    W = pd.Series(W)
    H = pd.Series(H)
    w_min = W.min()
    h_min = H.min()
    
    for index, photo in enumerate(fichiers):
        nv_nom = f"{path1}/{index}.jpg" 
        image = Image.open(path1 + photo)
        dimensionnement(image, w_min, h_min, nv_nom)
        
        
print(formatage(path1, path2))
