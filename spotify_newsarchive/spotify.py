""" 
Script to scroll through the Spotify newsroom (click on "load more" subsequently)
"""


# import relevant modules
from selenium import webdriver
import time

# open webdriver (needed, because rain info is only displayed when hovered over..)
def init():
    global browser
    browser = webdriver.Chrome()
    browser.get('file:///c:/projects/scraping_workshop/spotify_newsarchive/Spotify%20%E2%80%94%20For%20the%20Record.html')
    browser.implicitly_wait(3)

articles = browser.find_elements_by_class_name('recent-header')

f=open('articles.csv', 'w', encoding='UTF-8')

for art in articles:
    splitobj = art.text.split('\n')
    f.write(splitobj[0]+'\t'+splitobj[-1]+'\t'+art.find_elements_by_css_selector('*')[2].get_attribute('href')+'\n')

f.close()
