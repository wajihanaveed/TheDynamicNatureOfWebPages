from bs4 import BeautifulSoup
import requests
import lxml

# headers = {
#   "User-Agent":
#   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
# }

# html = requests.get('https://stackoverflow.com/questions/13423219/finding-ads-on-a-web-page', headers=headers).text

# soup = BeautifulSoup(html, 'lxml')

# for link in soup.findAll('div', class_='RnJeZd top pla-unit-title'):
#   print("THIS RUNS")
#   ad_link = link.a['href']
#   print(f'https://www.googleadservices.com/pagead{ad_link}')

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Firefox()
driver.get("https://www.dawn.com/")
driver.implicitly_wait(10)

iFrame = driver.find_element("tag name","iframe")
driver.switch_to.frame(iFrame)

try:
    #element = driver.find_element_by_css_selector("amp-img[class^='img_ad']")
    #print(element.get_attribute('outerHTML'))
    element = driver.find_element("name","aw0")
    print(element.get_attribute('innerHTML'))
except NoSuchElementException:
    print("Advert not found")
    print(driver.page_source)

driver.quit()