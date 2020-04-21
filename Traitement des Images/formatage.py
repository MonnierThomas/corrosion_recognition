from PIL import Image
import numpy as np
imgpil = Image.open("chat.jpg")  
#jsp comment aller lui faire chercher les images au bon endroit

def dimensionnement(image, W, H, Q):
    image = image.resize((W, H),Image.ANTIALIAS)
    image.save(f"{image}"+"new", quality=Q)
    #en vrai faut rajouter le path où tu veux l'enregistrer avant son nom
    

