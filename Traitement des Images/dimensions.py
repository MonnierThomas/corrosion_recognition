N = 20 #nombre d'images dans le dossier

from PIL import Image
import pandas as pd
#on va créer 2 séries: les hauteurs et les largeurs

def dimension(N):
    W = []
    H = []
    
    for i in range(N):
        img = Image.open(f"path/{i}.jpg")
        (w, h) = img.size
        W.append(w)
        H.append(h)
        
    W = pd.Series(W)
    H = pd.Series(H)
    w_min = W.min()
    h_min = H.min()
    return(w_min, h_min)

print(dimension(N))
