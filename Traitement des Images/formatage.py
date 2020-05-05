path1 = '' #entry path
path2 = '' #save path

from os import listdir
from os.path import isfile, join

from PIL import Image
import pandas as pd


def dimensionnement(image, W, H, nv_nom):
    image = image.resize((W, H), Image.ANTIALIAS)
    image.save(path2 + "/" + nv_nom, quality=95)



def formatage(path1, path2):
    """path1 est le chemin vers le dossier regroupant les photos originales, path2 le chemin d'arrivée"""
    
    #on commence par chercher les tailles finales de nos images
    fichiers = [f for f in listdir(path1) if isfile(join(path1, f))]
    fichiers.pop(0)
    #print(fichiers)
    W = []
    H = []
    
    for photo in fichiers:
        img = Image.open(path1 +"/"+ photo)
        (w, h) = img.size
        W.append(w)
        H.append(h)
        
    W = pd.Series(W)
    H = pd.Series(H)
    w_min = W.min()
    h_min = H.min()
    
    for photo in fichiers:
        nv_nom = "nouveau" +f"{photo}" +".jpg" 
        image = Image.open(path1 +"/"+ photo)
        dimensionnement(image, w_min, h_min, nv_nom)

formatage(path1, path2)


#Pour windows
#def dimensionnement(image, W, H, nv_nom):
#    image = image.resize((W, H), Image.ANTIALIAS)
#    if image.mode in ('RGBA', 'LA'):
#        background = Image.new(image.mode[:-1], image.size)
#        background.paste(image, image.split()[-1])
#        image = background
#    image.save(path2 + "/" + nv_nom, quality=95)
