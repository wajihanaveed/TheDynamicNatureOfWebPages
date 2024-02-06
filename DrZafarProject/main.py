import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd

# Function to download all iframes from a given list of images and store in a DataFrame
def getIframes(soup,url):
    data = []
    iframes = soup.find_all('iframe')
    print("The iframes are ",iframes)

    # Create a list of iframe sources
    iframe_sources = [iframe['src'] for iframe in iframes]

    # Add the iframe sources to the data list
    data.append({'Image URL': url, 'IFrame Sources': iframe_sources})


def download_iframes_to_dataframe(image_urls):
    data = []
    
    for image_url in image_urls:
        # Send an HTTP GET request to the image URL
        response = requests.get(image_url)

        if response.status_code == 200:
            # Parse the HTML content of the image URL
            soup = BeautifulSoup(response.text, 'html.parser')
            a=getIframes(soup,image_url)
        else:
            print("error in loading webpage")
    # Convert the data list to a Pandas DataFrame
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # List of image URLs
    image_urls = [
        'https://www.dawn.com/',
    ]

    # Call the function to download iframes and store in a DataFrame
    iframe_df = download_iframes_to_dataframe(image_urls)

    # Display the DataFrame
    print(iframe_df)
