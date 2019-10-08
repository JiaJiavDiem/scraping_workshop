""" 
RvB 20190719

Script for scraping buienradar's rain predictions.

Note:
    1. A webdriver needs to be downloaded for selenium to work. 
        The corresponding executable_path parameter must be set to proper location.
    2. Selenium is needed because buienradar does not provide rain data directly.
        First some cookies need to be accepted.
        Then one must hover over the graph to extract the values.
    3. For some reason predicted times are not always in time steps of 5 minutes.
        Sometimes it's 30 minutes (especially at start). Unclear to me why..
    4. Several sleep commands are used to either load the web page 
        or to start scraping at a proper time.
    5. Resulting dataframe should be manipulated for further use.
    6. No specific city is selected now.
        Can poosibly be solved by adjusting the url
        Or add another selenium command that enters the city name into the lookup box.
"""


# import relevant modules
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import scrapy
import pandas as pd
import datetime as dt

# set parameters
i_nr_minutes_between_measurement = 2
fn_json = 'output.json'


# open webdriver (needed, because rain info is only displayed when hovered over..)
def init():
    global browser
    browser = webdriver.Chrome() #put it in path instead (?) executable_path=r'chromedriver.exe')
    
    browser.get('https://www.buienradar.nl/')
    browser.implicitly_wait(3)

    # accept/reject cookies and other things
    browser.find_element_by_xpath('//div[@class="accept-button-block"]').click()
    browser.find_element_by_xpath('//a[@class="onboard-button button-no"]').click()


def get_forecast(lat=51.7, lon=5.3):
    global browser
    url='https://graphdata.buienradar.nl/forecast/json/?lat='+str(lat)+'&lon='+str(lon)
    browser.get(url)
    time.sleep(1)
    result = browser.page_source.replace('</pre></body></html>','').replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">','')
    return(result)

def reset():
    f=open(fn_json,'w', encoding='utf-8')
    f.close()

def run():
    while 1==1:
        try:
            print('getting forecast')
            res=get_forecast()
            print('writing to file')
            f=open(fn_json,'a', encoding='utf-8')
            f.write(res+'\n')
            f.close()
        except:
            print('error downloading forecast')
        print('sleeping')
        time.sleep(i_nr_minutes_between_measurement*60)

#browser.quit()


