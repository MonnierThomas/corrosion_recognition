

from os import listdir
from os.path import isfile, join



from PIL import Image
import pandas as pd

def dimensionnement(image, W, H, nv_nom):
    image = image.resize((W, H),Image.ANTIALIAS)
    image.save(nv_nom, quality=95)



def formatage(path1, path2):
    """path1 est le chemin vers le dossier regroupant les photos originales, path2 le chemin d'arrivée"""
    
    #on commence par chercher les tailles finales de nos images
    fichiers = [f for f in listdir(path1) if isfile(join(path1, f))]
    W = []
    H = []
    
    for photo in fichiers:
        img = Image.open(f"{photo}")
        (w, h) = img.size
        W.append(w)
        H.append(h)
        
    W = pd.Series(W)
    H = pd.Series(H)
    w_min = W.min()
    h_min = H.min()
    
    i = 0
    for photo in fichiers:
        nv_nom = path2 + f"{i}"
        dimensionnement(photo, w_min, h_min, nv_nom)


        


