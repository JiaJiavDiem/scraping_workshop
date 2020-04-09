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
    
    browser.get('https://newsroom.spotify.com/')
    browser.implicitly_wait(3)


def click():
    button=browser.find_element_by_class_name('load-more')
    button.click()
    
def loop():
    while 1==1:
        try:
            click()
            time.sleep(3)
        except:
            time.sleep(1)

init()
time.sleep(10)
loop()