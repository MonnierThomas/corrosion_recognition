# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:49:14 2020

@author: Thomas MONNIER
"""

from selenium import webdriver
import os
import requests
import shutil

searchterm = 'Okocha'#input your search item here
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
print(imges)
print(len(imges))

for image_url in imges:
    # Open the url image, set stream to True, this will return the stream content.
    resp = requests.get(image_url, stream=True)
    # Open a local file with wb ( write binary ) permission.
    local_file = open('local_image.jpg', 'wb')
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
    resp.raw.decode_content = True
    # Copy the response stream raw data to local image file.
    shutil.copyfileobj(resp.raw, local_file)
    # Remove the image url response object.
    del resp
