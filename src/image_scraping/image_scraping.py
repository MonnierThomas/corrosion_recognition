from selenium import webdriver
import os
import requests
import shutil
import argparse
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

def get_url(searchterm):
    '''
    Gets Google Images' URL for one keyword in the keyword list
    
    Input : searchterms : list of strings corresponding to the keywords
    Output : imges : list of strings corresponding to the URLs of the images
    '''

    url = "https://www.google.co.in/search?q="+searchterm+"&source=lnms&tbm=isch"
    browser = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options) # insert path to chromedriver inside parentheses
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
    
    
    
def download_image(searchterm, image_url, i):
    '''
    Downloads the images
    
    Input : image_url : string
            i : int
    '''
    # Opens the URL of the image, sets the stream to True and returns the content of the stream
    resp = requests.get(image_url, stream=True)
    # Opens local file
    local_file = open(f'{searchterm}/{i}.jpg', 'wb')
    # Defines decode_content as True to prevent image size equals to 0
    resp.raw.decode_content = True
    # Copies raw data in local file
    shutil.copyfileobj(resp.raw, local_file)
    # Deletes the image URL response object
    del resp
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keywords",
                        help="keywords",
                        nargs="+",
                        required=True)
    args = parser.parse_args()

    searchterms = []
    for keyword in args.keywords:
        searchterms.append(keyword)
    
    for searchterm in searchterms:
        imges = get_url(searchterm)

        for i, image_url in enumerate(imges):
            download_image(searchterm, image_url, i)