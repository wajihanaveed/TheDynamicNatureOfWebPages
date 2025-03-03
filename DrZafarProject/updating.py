#https://stackoverflow.com/questions/23223018/selenium-get-all-iframes-in-a-page-even-nested-ones


###############
# THIS CODE DOWNLOADS ALL THE IMAGES / BE CAREFUL
# list of add_Webites: https://pgl.yoyo.org/as/serverlist.php?hostformat=hosts
# web crawler library for ads: https://github.com/UWCSESecurityLab/adscraper/blob/main/crawler/src/crawler.ts
# Broad website crawler Library
#####################################
from bs4 import *
import requests
import os
def folder_create(images):
    folder_name = input("Enter name of folder: ")
    os.mkdir(folder_name)
    download_images(images, folder_name)
def download_images(images, folder_name):
    count = 0
    print(f"Found {len(images)} images")
    if len(images) != 0:
        for i, image in enumerate(images):
            image_link = image["src"]
            r = requests.get(image_link).content
            with open(f"{folder_name}/images{i+1}.jpg", "wb+") as f:
                f.write(r)
                count += 1
        if count == len(images):
            print("All the images have been downloaded!")
        else:
            print(f" {count} images have been downloaded out of {len(images)}")
def main(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.findAll('img')
    folder_create(images)
url = input("Enter site URL:")
main(url)

