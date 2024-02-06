import requests
from bs4 import BeautifulSoup
import os

website_url = 'https://www.dawn.com/'
response = requests.get(website_url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    css_dir = 'css'
    js_dir = 'js'
    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(js_dir, exist_ok=True)

    # Find and download CSS files
    css_links = [link.get('href') for link in soup.find_all('link', rel='stylesheet')]
    for css_link in css_links:
        css_url = website_url + css_link if not css_link.startswith('http') else css_link
        css_response = requests.get(css_url)
        if css_response.status_code == 200:
            print(os.path.basename(css_url))
            #git print(css_response.content)
            with open(css_dir, 'w') as css_file:
                css_file.write(css_response.content)

    # Find and download JavaScript files
    js_links = [script.get('src') for script in soup.find_all('script', src=True)]
    for js_link in js_links:
        js_url = website_url + js_link if not js_link.startswith('http') else js_link
        js_response = requests.get(js_url)
        if js_response.status_code == 200:
            #print(js_response.content)
            with open(os.path.join(js_dir, os.path.basename(js_url)), 'wb') as js_file:
                js_file.write(js_response.content)

    print("CSS and JavaScript files downloaded successfully.")
else:
    print(f"Failed to retrieve the website. Status code: {response.status_code}")
