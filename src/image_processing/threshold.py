from os import listdir, makedirs
from os.path import isfile, join
from PIL import Image
from image_processing.image_processing import dimension, formatage, symetries, pre_tri, tri
from math import sqrt
import numpy as np

path = "" # enter the path with the image processing module
import sys
sys.path.append(path)

path = ""

# median of the image size
m = 455200

def treshold_by_size():
    """
    Sorts images in 2 categories: below and above the median, and format them to the average size of each sub-category
    """
    files = [f for f in listdir(path) if isfile(join(path, f))]  
    path_small = path + "/small_images"
    path_large = path + "/large_images"
    makedirs(path_small)
    makedirs(path_large)
    
    # Sorts by size
    for image in files:
        if image != ".DS_Store":
            image = Image.open(path + "/" + image)
            a, b = image.size
            if a*b < m:
                image.save(path_small+"/"+image, quality=95)
            else:
                image.save(path_large+"/"+image, quality=95)
                
    # Formats
    W, H, Tp = dimension(path_small)
    tp = np.mean(Tp)
    cp = int(sqrt(tp))    
    W, H, Tg = dimension(path_large)
    tg = np.mean(Tg)
    cg = int(sqrt(tg))    
    path_small_output = path_small + "/outputs"
    makedirs(path_small_output)
    path_large_output = path_large + "/outputs"
    makedirs(path_large_output)    
    formatage((cp,cp), path_small, path_small_output)
    formatage((cg,cg), path_large, path_large_output)
    
    # Symmetry to multiply the dataset's size by 4
    symetries(path_small_output)
    symetries(path_large_output)
    
    # Repartition in train / validation / test   
    pre_tri(path_small_output)
    pre_tri(path_large_output)
    tri(path_small_output)
    tri(path_large_output)
   
if __name__ == '__main__' :
    treshold_by_size()