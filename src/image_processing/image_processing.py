from os import listdir, makedirs, remove
from os.path import isfile, join
from PIL import Image


def join_photos(path1, path2):
    """Enregistre les images classées par dossier dans un seul et même dossier en les renommant suivant leur dossier d'origine
    Entrée: path1: chaîne de caractères, chemin vers les données brutes classées par mot-clé
              path2: chaîne de caractères, chemin vers le dossier où on enregistre toutes les images ensembles"""
    dossiers = [f for f in listdir(path1)]
    for dossier in dossiers:
        if dossier != ".DS_Store":
            path = path1+"/"+dossier
            images = [f for f in listdir(path) if isfile(join(path,f))]
            if len(images) <=1:
                #le dossier contient d'autres dossiers
                sous_dossiers = [f for f in listdir(path)]
                for fichier in sous_dossiers:
                    if fichier != ".DS_Store":
                        path_bis = path + "/" + fichier
                        images = [f for f in listdir(path_bis) if isfile(join(path_bis,f))]
                        for image in images:
                            if image != ".DS_Store":
                                img = Image.open(path_bis+"/"+image)
                                if img.mode != 'RGB':
                                    img = img.convert('RGB')
                                img.save(path2 + "/" + fichier + image , quality = 95)
            else:
                for image in images:
                    if image != ".DS_Store":
                            img = Image.open(path+"/"+image)
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            img.save(path2 + "/" + dossier + image , quality = 95)

def dimension(chemin):
    """Entrée: chemin vers le dossier d'images (chaîne de caractères)
    Sortie: liste des largeurs, hauteurs et tailles des images en pixels classées par ordre croissant"""
    W = []
    #liste des largeurs
    H = []
    #liste des hauteurs
    T = []
    #liste des tailles
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
    return(W, H, T)

def formatage(taille, path1, path2):
    """Formate notre ensemble d'images brutes et les met à la taille souhaitée
    Entrée: taille: entier
            path1: chaîne de caractères, dossier d'images brutes
            path2: chaîne de caractères, dossier d'images formatées"""
    fichiers = [f for f in listdir(path1) if isfile(join(path1, f))]       
    for photo in fichiers:
        if photo!=".DS_Store":
            nv_nom = "nouveau" +f"{photo}"
            image = Image.open(path1 +"/"+ photo)
            image = image.resize(taille, Image.ANTIALIAS)
            image.save(path2 + "/" + nv_nom, quality=95)

def symetrie_horizontale(path1, path2):
    """Enregistre la symétrie axiale horizontale d'une image
        Entrée: path1, chaîne de caractère, image de départ
                path2, chaîne de caractère, chemin où on enregistre l'image d'arrivée"""
    image = Image.open(path1)
    l, h = image.size
    image_sym = Image.new("RGB", (l, h))
    #on va construire l'image pixel par pixel    
    for i in range(l):
        for j in range(h):
            p = image.getpixel((i,j))
            image_sym.putpixel((i, h-1-j), p)    
    image_sym.save(path2)

def symetrie_verticale(path1, path2):
    """Enregistre la symétrie axiale verticale d'une image
        Entrée: path1, chaîne de caractère, image de départ
                path2, chaîne de caractère, chemin où on enregistre l'image d'arrivée"""
    image = Image.open(path1)
    l, h = image.size
    image_sym = Image.new("RGB", (l, h))    
    for i in range(l):
        for j in range(h):
            p = image.getpixel((i, j))
            image_sym.putpixel((l-1-i, j), p)
    image_sym.save(path2)
    

def symetries(path):
    """Enregistre les symétries axiales verticales et horizontales de l'ensemble des images d'un dossier dans ce même dossier
    Entrée: dossier d'images, chaîne de caractères"""
    fichiers = [f for f in listdir(path) if isfile(join(path, f))]
    for photo in fichiers:
        if photo != ".DS_Store":
            path1 = path + "/" + photo
            path2 = path + "/" + "symh" + photo
            path3 = path + "/" + "symv" + photo
            symetrie_horizontale(path1, path2)
            symetrie_verticale(path1, path3)
            symetrie_verticale(path2, path3)
            

def is_corr(photo):
    """indique la présence de "corr" dans une chaîne de caractère
    Entrée: chaîne de caractère"""
    i = 0
    while i < len(photo):
        if [photo[i+k] for k in range(4)] == ["c", "o", "r", "r"]:
            return(True)
        i = i +1
    return(False)
        
def pre_tri(path):
    """Trie les images d'un dossier en 2 sous-dossier: CORROSION ET NON CORROSION, suivant leur nom
    Entrée: dossier d'images, chaîne de caractères"""
    path_corrosion = path + "/" + "CORROSION"
    path_non_corr = path + "/" + "NON CORROSION"
    makedirs(path_corrosion)
    makedirs(path_non_corr)
    fichiers = [f for f in listdir(path) if isfile(join(path, f))]
    for photo in fichiers:
        if photo != ".DS_Store":
            image = Image.open(path + "/" + photo)
            if is_corr(photo):
                image.save(path_corrosion + "/" + photo)
            else:
                image.save(path_non_corr + "/" + photo)
            remove(path + "/" + photo)
        


def tri(path):
    """Répartit chaque set d'images (CORROSION ET NON CORROSION) en trois ensembles: Entrainement (7/8 environ), Validation (1/8 environ) et Test (1/100 environ)
    Entrée: dossier d'iamges (qui contient les sous-dossiers CORROSION et NON CORROSION, chaîne de caractères"""
    path_entrain = path + "/" + "Entrainement"
    path_validation = path + "/" + "Validation"
    path_test = path + "/" + "Test"
    path_corrosion = path + "/CORROSION"
    path_non_corr = path + "/NON CORROSION"
    
    makedirs(path_entrain)
    #contiendra environ 7/8 de nos images
    makedirs(path_validation)
    #contiendra environ 1/8 de nos images
    makedirs(path_test)
    #contiendra environ 1/100 des images
    
    #on s'occupe d'abord de la corrosion
    makedirs(path_entrain + "/" + "corrosion")
    makedirs(path_validation + "/" + "corrosion")
    makedirs(path_test + "/" + "corrosion")
    fichiers = [f for f in listdir(path_corrosion)]
    i = 1
    for photo in fichiers:
        if photo != ".DS_Store":
            image = Image.open(path_corrosion + "/" + photo)
            if i % 100 == 0:
                image.save(path_test + "/" + "corrosion" + "/" + photo, quality=95)
            elif i % 8 != 0:
                image.save(path_entrain + "/" + "corrosion" + "/" + photo, quality=95)
            else:
                image.save(path_validation + "/" + "corrosion" + "/" + photo, quality=95)
            i = i + 1
    
    #non corrosion
    makedirs(path_entrain + "/" + "non corrosion")
    makedirs(path_validation + "/" + "non corrosion")
    makedirs(path_test + "/" + "non corrosion")
    fichiers = [f for f in listdir(path_non_corr)]
    i = 1
    for photo in fichiers:
        if photo != ".DS_Store":
            image = Image.open(path_non_corr + "/" + photo)
            if i % 100 == 0:
                image.save(path_test + "/" + "non corrosion" + "/" + photo, quality=95)
            elif i % 8 != 0:
                image.save(path_entrain + "/" + "non corrosion" + "/" + photo, quality=95)
            else:
                image.save(path_validation + "/" + "non corrosion" + "/" + photo, quality=95)
            i = i+1
            

def main():
    path_dossiers = #le chemin où sont enregistrées nos images brutes par dossiers
    path_brutes = #le chemin où on veut mettre nos images brutes ensembles
    path_formatees = #le chemin où on veut mettre nos images formatées et où on trouvera les dossiers utiles
    taille = #la taille choisie après étude des dimensions de l'ensemble d'images brutes
    join_photos(path_dossiers, path_brutes)
    formatage(taille, path_brutes, path_formatees)
    symetries(path_formatees)
    pre_tri(path_formatees)
    tri(path_formatees)

    
main()
