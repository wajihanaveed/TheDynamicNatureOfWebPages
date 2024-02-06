# compares if the css files are identidal 
import requests
from bs4 import BeautifulSoup
import cssutils
import time

def download_css(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_css(css_text):
    sheet = cssutils.css.CSSStyleSheet()
    sheet.cssText = css_text
    return sheet

def compare_css(css1, css2):
    return css1.cssText == css2.cssText

def main():
    url1 = "https://example.com/style.css"  # Replace with the actual URL of the first CSS file
    url2 = "https://anotherexample.com/style.css"  # Replace with the actual URL of the second CSS file

    while True:
        css1 = download_css(url1)
        css2 = download_css(url2)

        if css1 is not None and css2 is not None:
            parsed_css1 = parse_css(css1)
            parsed_css2 = parse_css(css2)

            if compare_css(parsed_css1, parsed_css2):
                print("CSS styles are the same.")
            else:
                print("CSS styles are different.")

        else:
            print("Failed to download CSS from one or both URLs.")

        time.sleep(60)  # Wait for a minute before checking again

if __name__ == "__main__":
    main()
