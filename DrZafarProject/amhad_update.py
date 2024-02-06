import requests
import time
import random
from bs4 import BeautifulSoup
import difflib
import re
import wget
# Website URL to monitor
website_url = "https://www.bbc.com"

# Time interval for each download. Randomize to prevent bot detection.
download_interval = 10

# Duration of monitoring (in seconds)
monitoring_duration = 60 * 5


def download_html(url):
    print("Sending request...")
    try:
        response = requests.get(url)
    except:
        print(
            f"Failed to contact website after maximum retries...")
        return None

    if response.status_code == 200:
        return response.text
    else:
        print("Failed to download HTML")
        return None


def extract_img_srcs(html):
    # print(html)
    if html == None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    img_srcs = [img['src'] for img in soup.find_all('img', src=True)]
    print(f"First 5 img sources: {img_srcs[:5]}")
    return img_srcs


def extract_iframe_srcs(html):
    if html == None:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    iframe_srcs = [iframe['src']
                   for iframe in soup.find_all('iframe', src=True)]
    print(f"First 5 iframe sources: {iframe_srcs[:5]}")
    return iframe_srcs

def getGifs(soup):
    # change this code we can't seem to find the gifs
    gif_tags = soup.find_all("img", src=re.compile(r".*\.gif"))

    for gif_tag in gif_tags:
        gif_url = gif_tag["src"]
        # Download the GIF to the current working directory
        wget.download(gif_url)
        print(f"Downloaded: {gif_url}")
    return gif_tag



def main_loop():
    global download_interval
    start_time = time.time()
    
    prev_html = download_html(website_url)
    prev_html = BeautifulSoup(prev_html, 'html.parser')
    prev_img_srcs = extract_img_srcs(prev_html)
    prev_iframe_srcs = extract_iframe_srcs(prev_html)
    prev_gif_srcs=getGifs(soup)
    update_count = 0
    num_of_successes = 0
    num_of_fails = 0

    while time.time() - start_time < monitoring_duration:
        time.sleep(download_interval)
        current_html = download_html(website_url)
        if current_html != None:
            num_of_successes += 1
        else:
            num_of_fails += 1
            continue
        soup = BeautifulSoup(current_html, 'html.parser')
        current_img_srcs = extract_img_srcs(current_html)
        current_iframe_srcs = extract_iframe_srcs(current_html)

        if (current_iframe_srcs and current_img_srcs) and (current_img_srcs != prev_img_srcs or current_iframe_srcs != prev_iframe_srcs):
            update_count += 1
            print(f"Website updated! Update count: {update_count}")

            print("Changes in <img> src attributes:")
            for diff in difflib.ndiff(prev_img_srcs, current_img_srcs):
                if diff.startswith('+ '):
                    print("Added:", diff[2:])
                elif diff.startswith('- '):
                    print("Removed:", diff[2:])

            print("Changes in <iframe> src attributes:")
            for diff in difflib.ndiff(prev_iframe_srcs, current_iframe_srcs):
                if diff.startswith('+ '):
                    print("Added:", diff[2:])
                elif diff.startswith('- '):
                    print("Removed:", diff[2:])
            prev_img_srcs = current_img_srcs
            prev_iframe_srcs = current_iframe_srcs

        download_interval = random.randint(0, 15)

    print(f"Monitoring complete!")
    print("Statistics:")
    print(f"Number of successful requests: {num_of_successes}")
    print(f"Number of failed requests: {num_of_fails}")
    print(f"Number of updates to image soruces: {update_count}")


main_loop()
