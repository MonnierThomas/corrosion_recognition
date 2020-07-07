from selenium import webdriver
import os
import requests
import shutil

def get_url(searchterms):
    '''Obtient l'URL des images de Google Images pour chaque mot-clé compris dans la liste des mots-clés
    
    Input : searchterms : liste de chaines de caractère correspondant aux mots clés
    
    Output : imges : liste de chaines de caractère correspondant aux URL des images
    '''
    
    for searchterm in searchterms:
        url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
        browser = webdriver.Chrome()#insert path to chromedriver inside parentheses
        browser.get(url)
        img_count = 0
        extensions = { "jpg", "jpeg", "png", "gif" }
        if not os.path.exists(searchterm):
            os.mkdir(searchterm)
    
    for _ in range(500):
        browser.execute_script("window.scrollBy(0,10000)")
        
    html = browser.page_source.split('["')
    imges = []
    for i in html:
        if i.startswith('http') and i.split('"')[0].split('.')[-1] in extensions:
            imges.append(i.split('"')[0])
    return imges
    
    
    
def download_image(image_url, i):
    ''' Télécharge les images
    
    Input : image_url : chaine de caractère
            i : int
    '''
    # Ouvre l'URL de l'image, définis le flux sur Vrai et retourne le contenu du flux
    resp = requests.get(image_url, stream=True)
    # Ouvre un fichier local grâce à 'wb'
    local_file = open(f'{i}.jpg', 'wb')
    # Définis decode_content comme Vrai, sinon la taille de l'image téléchargée serait de 0
    resp.raw.decode_content = True
    # Copie les données brutes du flux de réponses dans un fichier image local
    shutil.copyfileobj(resp.raw, local_file)
    # Supprimez l'objet de réponse d'URL d'image
    del resp
    
    
    
def main():
    searchterms = [] # Liste des mots-clés souhaités
    imges = get_url(searchterms)
    for i, image_url in enumerate(imges):
        download_image(image_url, i)
        
        
main()
