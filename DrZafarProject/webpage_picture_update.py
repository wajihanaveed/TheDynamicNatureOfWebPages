import requests
import time
from bs4 import BeautifulSoup
import difflib
import wget
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException



# Website URL to monitor
website_url = "https://www.bbc.com"

# Time interval 2 each download (in seconds)
download_interval = 60

# Duration of monitoring (in seconds)
monitoring_duration = 30

def download_html(url):
    print("The Html is being Downloaded")
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to download HTML")
        return None

def extract_img_srcs(soup):
    print("Entrypoint: extract_img_srcs")

    # print(html)
    # print(soup)
    img_srcs = [img['src'] for img in soup.find_all('img', src=True)]
    print(img_srcs)
    return img_srcs

def getIframeSrc(url):
    print("Entrypoint: getIframeSrc ")
    driver = webdriver.Firefox()
    driver.get(url)
    driver.implicitly_wait(2)
    iFrame = driver.find_element("tag name","iframe")
    driver.switch_to.frame(iFrame)
    iframeSrc=[]
    try:
        # element = driver.find_element_by_css_selector("amp-img[class^='img_ad']")
        # print(element.get_attribute('outerHTML'))
        driver.implicitly_wait(1)
        element = driver.find_element("name","aw0")
        iframeSrc=element.get_attribute('innerHTML')
    except NoSuchElementException:
        print("Advert not found")
        print(driver.page_source)

    driver.quit()
    print("Exitpoint: getIframeSrc")
    return iframeSrc

def getGifs(soup):
    print("Entrypoint: getGifs")
    # change this code we can't seem to find the gifs
    gif_tags = soup.find_all("img", src=re.compile(r".*\.gif"))
    for gif_tag in gif_tags:
        gif_url = gif_tag["src"]
        # Download the GIF to the current working directory
        wget.download(gif_url)
        print(f"Downloaded: {gif_url}")


# reminder: move data to csv
def main():

    start_time = time.time()

    # This downloads the first HTML
    prev_html = download_html(website_url)
    soup = BeautifulSoup(prev_html, 'html.parser')
    # The image sources for the first html are extraced
    prev_img_srcs = extract_img_srcs(soup)
    # THE Iframes are extraced
    prev_iframe_src=getIframeSrc(website_url)
    update_count = 0
    
    while time.time() - start_time < monitoring_duration:
        # wait for the required interval
        time.sleep(download_interval)
        # download the updated html
        updated_html = download_html(website_url)
        soup = BeautifulSoup(updated_html, 'html.parser')
        current_img_srcs = extract_img_srcs(soup)
        iFrameData=getIframeSrc(website_url)
        # comparison protion
        if updated_html and current_img_srcs != prev_img_srcs:
            update_count += 1
            print(f"Website updated! Update count: {update_count}")
            print("Changes in <img> src attributes:")
            for diff in difflib.ndiff(prev_img_srcs, current_img_srcs):
                if diff.startswith('+ '):
                    print("Added:", diff[2:])
                elif diff.startswith('- '):
                    print("Removed:", diff[2:])
            
            prev_img_srcs = current_img_srcs
    
    print(f"Monitoring complete. Total updates: {update_count}")

if __name__ == "__main__":
    main()
