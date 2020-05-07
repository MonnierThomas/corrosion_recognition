#CONSTITUTION DES BATCHS TESTS / ENTRAINEMENT
#0,8 APPRENTISSAGE, 0,2 TEST

path = "/Users/charlotte/Desktop/Cours Mines/Informatique/Projet info 3/Traitement des Images/photos_formatees"
path_corrosion = "/Users/charlotte/Desktop/Cours Mines/Informatique/Projet info 3/Traitement des Images/photos_formatees/CORROSION"
path_non_corr = "/Users/charlotte/Desktop/Cours Mines/Informatique/Projet info 3/Traitement des Images/photos_formatees/NON CORROSION"

#on va faire 2 dossiers, et les séparer au sein de chaque dossier

from os import listdir, makedirs
from os.path import isfile, join

from PIL import Image

path_entrain = path + "/" + "Entrainement"
path_test = path + "/" + "Test"

makedirs(path_entrain)
makedirs(path_test)
#on s'occupe d'abord de la corrosion
makedirs(path_entrain + "/" + "corrosion")
makedirs(path_test + "/" + "corrosion")
fichiers = [f for f in listdir(path_corrosion)]
for dossier in fichiers:
    if dossier != ".DS_Store":
        photos = [f for f in listdir(path_corrosion+"/"+dossier)]
        i = 1
        for photo in photos:
            if photo != ".DS_Store":
                image = Image.open(path_corrosion + "/" + dossier + "/" + photo)
                if i % 8 != 0:
                    image.save(path_entrain + "/" + "corrosion" + "/" + photo +".jpg", quality=95)
                else:
                    image.save(path_test + "/" + "corrosion" + "/" + photo + ".jpg", quality=95)
                i = i+1



#non corrosion
makedirs(path_entrain + "/" + "non corrosion")
makedirs(path_test + "/" + "non corrosion")

fichiers = [f for f in listdir(path_non_corr)]
for dossier in fichiers:
    if dossier != ".DS_Store":
        photos = [f for f in listdir(path_non_corr+"/"+dossier)]
        i = 1
        for photo in photos:
            if photo != ".DS_Store":
                image = Image.open(path_non_corr + "/" + dossier + "/" + photo)
                if i % 8 != 0:
                    image.save(path_entrain + "/" + "non corrosion" + "/" + photo +".jpg", quality=95)
                else:
                    image.save(path_test + "/" + "non corrosion" + "/" + photo + ".jpg", quality=95)
                i = i+1


