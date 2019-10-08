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

# open webdriver (needed, because rain info is only displayed when hovered over..)
browser = webdriver.Chrome(executable_path=r'C:\webdrivers\chromedriver.exe')

browser.get('https://www.buienradar.nl/')
browser.implicitly_wait(3)

# accept/reject cookies and other things
browser.find_element_by_xpath('//div[@class="accept-button-block"]').click()
browser.find_element_by_xpath('//a[@class="onboard-button button-no"]').click()

# initialize loop variables
bool_keep_scraping = True
dt_now = dt.datetime.now()
dt_now_minutes = dt.datetime(dt_now.year, 
                             dt_now.month,
                             dt_now.day,
                             dt_now.hour,
                             dt_now.minute)
dt_next = dt_now_minutes + dt.timedelta(minutes = 1) 
i_counter = 0
li_cols = ['time_measurement','time_prediction','value_prediction']
df_output = pd.DataFrame(columns = li_cols)

# start scraping
while bool_keep_scraping:
    # wait until full minute
    print(dt_next)
    time.sleep((dt_next - dt.datetime.now()).seconds)
    browser.refresh()
    time.sleep(3)

    # go to graph
    element_to_hover_over = browser.find_element_by_xpath('//div[@class="graph"]')
    hover = ActionChains(browser).move_to_element_with_offset(element_to_hover_over, 1 , 20)
    hover.perform()
    
    # initialize df_output_to_add input variables
    li_measurement = []
    li_time = []
    li_rain = []

    # hover from left to right to get updated html
    for i_hovers in range(80):
        hover = ActionChains(browser).move_by_offset(5,0)
        hover.perform()
        time.sleep(.5)
        
        html_source = browser.page_source
        sel = scrapy.Selector(text = html_source)
        
        try:
            # try needed because span object can not always be found (in particular first observation)
            str_time = sel.xpath('//span[@class="time"]/text()').extract()[0]
            str_rain = sel.xpath('//span[@class="rain"]/text()').extract()[0]
            li_measurement.append(dt_next)
            li_time.append(str_time)
            li_rain.append(str_rain)
        except:
            pass
    
    # turn lists into dataframe (via dictionary)
    dict_output_to_add = {li_cols[0]: li_measurement,
                          li_cols[1]: li_time,
                          li_cols[2]: li_rain}
    df_to_add = pd.DataFrame.from_dict(dict_output_to_add)
    
    # remove duplicates, because hovering is not accurate enough to only get unique observations
    df_to_add = df_to_add.drop_duplicates()
            
    # append output
    df_output = pd.concat([df_output, df_to_add], ignore_index = True)
    
    dt_next = dt_next + dt.timedelta(minutes = i_nr_minutes_between_measurement)
    
    # counter built to make it stop after 3 iterations
    i_counter += 1
    if i_counter > 2:
        bool_keep_scraping = False

browser.quit()


