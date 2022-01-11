from os import listdir, makedirs, remove
from os.path import isfile, join
from PIL import Image


def join_images(path1, path2):
    """
    Saves the images sorted by folder in a single folder, renaming them according to their original folder
    Input: path1: string, path to the raw data sorted by keyword
           path2: string, path to the folder where we save all the images together
    """
    folders = [f for f in listdir(path1)]
    for folder in folders:
        if folder != ".DS_Store":
            path = path1+"/"+folder
            images = [f for f in listdir(path) if isfile(join(path,f))]
            if len(images) <=1:
                sub_folders = [f for f in listdir(path)]
                for file in sub_folders:
                    if file != ".DS_Store":
                        path_bis = path + "/" + file
                        images = [f for f in listdir(path_bis) if isfile(join(path_bis,f))]
                        for image in images:
                            if image != ".DS_Store":
                                img = Image.open(path_bis+"/"+image)
                                if img.mode != 'RGB':
                                    img = img.convert('RGB')
                                img.save(path2 + "/" + file + image , quality = 95)
            else:
                for image in images:
                    if image != ".DS_Store":
                            img = Image.open(path+"/"+image)
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            img.save(path2 + "/" + folder + image , quality = 95)

def dimension(path):
    """
    Input:  path of the image folder (string)
    Output: list of widths, heights and sizes of the images in pixels sorted in ascending order
    """
    W = []
    H = []
    S = []
    files = [f for f in listdir(path) if isfile(join(path,f))]
    for image in files:
        if image != ".DS_Store":
            img = Image.open(path+"/"+image)
            (w, h) = img.size
            W.append(w)
            H.append(h)
            S.append(w*h)
    #on veut maintenant les trier dans l'ordre croissant
    W = sorted(W)
    H = sorted(H)
    return(W, H, S)

def formatage(size, path1, path2):
    """
    Formats our raw image set and set it to the desired size
    Input: size: integer
           path1: string, folder of raw images
           path2: string, formatted images folder
    """
    files = [f for f in listdir(path1) if isfile(join(path1, f))]       
    for image in files:
        if image!=".DS_Store":
            nv_nom = "new" +f"{image}"
            image = Image.open(path1 +"/"+ image)
            image = image.resize(size, Image.ANTIALIAS)
            image.save(path2 + "/" + nv_nom, quality=95)

def horizontal_symmetry(path1, path2):
    """
    Stores the horizontal axial symmetry of an image
        
    Input: path1, string, start image
           path2, string, path where you save the arrival image
    """
    image = Image.open(path1)
    l, h = image.size
    image_sym = Image.new("RGB", (l, h))
    #on va construire l'image pixel par pixel    
    for i in range(l):
        for j in range(h):
            p = image.getpixel((i,j))
            image_sym.putpixel((i, h-1-j), p)    
    image_sym.save(path2)

def vertical_symmetry(path1, path2):
    """
    Stores the vertical axial symmetry of an image
    
    Input: path1, string, start image
           path2, string, path where you save the final image
    """
    image = Image.open(path1)
    l, h = image.size
    image_sym = Image.new("RGB", (l, h))    
    for i in range(l):
        for j in range(h):
            p = image.getpixel((i, j))
            image_sym.putpixel((l-1-i, j), p)
    image_sym.save(path2)
    

def symmetries(path):
    """
    Saves the vertical and horizontal axial symmetries of all the images in a folder to the same folder
    Input: image folder, string
    """
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for image in files:
        if image != ".DS_Store":
            path1 = path + "/" + image
            path2 = path + "/" + "symh" + image
            path3 = path + "/" + "symv" + image
            horizontal_symmetry(path1, path2)
            vertical_symmetry(path1, path3)
            vertical_symmetry(path2, path3)
            

def is_corr(image):
    """
    Indicates the presence of "corr" in a string
    Input: string
    """
    i = 0
    while i < len(image):
        if [image[i+k] for k in range(4)] == ["c", "o", "r", "r"]:
            return(True)
        i = i +1
    return(False)
        
def pre_tri(path):
    """
    Sorts the images of a folder into 2 subfolders: CORROSION and UNCORROSION, according to their name
    Input: image folder, string
    """
    path_corrosion = path + "/" + "CORROSION"
    path_non_corr = path + "/" + "UNCORROSION"
    makedirs(path_corrosion)
    makedirs(path_non_corr)
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for image in files:
        if image != ".DS_Store":
            image = Image.open(path + "/" + image)
            if is_corr(image):
                image.save(path_corrosion + "/" + image)
            else:
                image.save(path_non_corr + "/" + image)
            remove(path + "/" + image)
        


def tri(path):
    """
    Divides each set of images (CORROSION and UNCORROSION) into three sets: Training (about 7/8), Validation (about 1/8) and Test (about 1/100)
    Input: images folder (which contains the CORROSION and UNCORROSION subfolders, string
    """
    train = path + "/" + "Training"
    validation = path + "/" + "Validation"
    test = path + "/" + "Test"
    path_corrosion = path + "/CORROSION"
    path_non_corr = path + "/UNCORROSION"
    
    makedirs(train)
    makedirs(validation)
    makedirs(test)
    
    # CORROSION
    makedirs(train + "/" + "corrosion")
    makedirs(validation + "/" + "corrosion")
    makedirs(test + "/" + "corrosion")
    files = [f for f in listdir(path_corrosion)]
    i = 1
    for image in files:
        if image != ".DS_Store":
            image = Image.open(path_corrosion + "/" + image)
            if i % 100 == 0:
                image.save(test + "/" + "corrosion" + "/" + image, quality=95)
            elif i % 8 != 0:
                image.save(train + "/" + "corrosion" + "/" + image, quality=95)
            else:
                image.save(validation + "/" + "corrosion" + "/" + image, quality=95)
            i = i + 1
    
    # UNCORROSION
    makedirs(train + "/" + "uncorrosion")
    makedirs(validation + "/" + "uncorrosion")
    makedirs(test + "/" + "uncorrosion")
    files = [f for f in listdir(path_non_corr)]
    i = 1
    for image in files:
        if image != ".DS_Store":
            image = Image.open(path_non_corr + "/" + image)
            if i % 100 == 0:
                image.save(test + "/" + "uncorrosion" + "/" + image, quality=95)
            elif i % 8 != 0:
                image.save(train + "/" + "uncorrosion" + "/" + image, quality=95)
            else:
                image.save(validation + "/" + "uncorrosion" + "/" + image, quality=95)
            i = i+1
            

if __name__ == '__main__' :
    folders = # raw data by folders
    raw = # raw data assembled
    output = # formated data
    size = # size chosen
    join_images(folders, raw)
    formatage(size, raw, output)
    symmetries(output)
    pre_tri(output)
    tri(output)