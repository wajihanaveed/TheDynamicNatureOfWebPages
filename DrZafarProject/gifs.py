import random
import requests
from bs4 import BeautifulSoup

########################################################
'''
potential Issue: There's a cookie page making sure the src page doesn't download
It's specific to this websire 
use re to get *.gif - done in webpage_picture_update
'''
# 
###########################################################
def download_file(url):
    local_filename = url.split('/')[-1]
    print("Downloading {} ---> {}".format(url, local_filename))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

def Download_Image_from_Web(url):
    
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    for link in soup.findAll('img'):
        print("this runs")
        image_links = link.get('src')
        if image_links.endswith('blank.gif'):
            image_links = link.get('data-lazy')
        if not image_links.startswith('http'):
            image_links = url + '/' + image_links
        download_file(image_links)

Download_Image_from_Web("https://pixabay.com/en/photos/?q=sleeping+puppy&hp=&image_type=&cat=&min_width=&min_height=")