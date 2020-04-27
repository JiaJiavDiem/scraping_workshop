#   __          __         _                         
#   \ \        / /        | |                        
#    \ \  /\  / /    ___  | |__                      
#     \ \/  \/ /    / _ \ | '_ \                     
#      \  /\  /    |  __/ | |_) |                    
#       \/  \/      \___| |_.__/                     
#    ___    ___   _ __    __ _   _ __     ___   _ __ 
#   / __|  / __| | '__|  / _` | | '_ \   / _ \ | '__|
#   \__ \ | (__  | |    | (_| | | |_) | |  __/ | |   
#   |___/  \___| |_|     \__,_| | .__/   \___| |_|   
#                               | |                  
#                               |_|                  

# Example webscraper for Bol.com

# Run these pip commands on your system before running the code:
# pip install lxml
# pip install selenium

# Download chromedriver.exe and put it in the directory of this code file
# https://sites.google.com/a/chromium.org/chromedriver/

# START OF PYTHON SCRIPT

# Load required packages
import urllib2
import datetime
from lxml import etree 
from selenium import webdriver
import time

listofproducts=['9200000045764367', '9200000006557118', '9200000030233201', '1004004013539792']
browser = webdriver.Chrome()

for targetproduct in listofproducts:
	# Assemble the correct URL
	baseurl = 'http://www.bol.com/nl/p/hello/'
	#targetproduct = '9200000006557118'
	complete_url = baseurl + targetproduct
	print(complete_url)

	# Open Chrome
	# Download webpage
	browser.get(complete_url)
	# Wait a bit... so that the website is fullly loaded
	time.sleep(5)
	# Convert page to something machine-readable
	tree = etree.fromstring(browser.page_source, parser=etree.HTMLParser()) # makes the website queryable

	# Convert website to readable stuff
	# --> Get XPATH of text that you would like to get
	xpath = '/html/body/div[2]/div[2]/div/div[2]/div[2]/div[1]/div[2]/div[1]/div[1]'

	# Parsing
	# Extract information
	information = etree.tostring(tree.xpath(xpath)[0])
	print(information)




