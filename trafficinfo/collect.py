# Load packages into memory
import requests
from tinydb import TinyDB
import json
import time
from datetime import datetime

dbname='traffic_db.json'

db = TinyDB(dbname)

def get():
    # Let's get the current VAT rate in the EU
    url = 'https://www.anwb.nl/feeds/gethf'
    routeInfo = requests.get(url, headers={})
    if (routeInfo.status_code==200):
        db.insert(json.loads(routeInfo.text))

def run():
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
    get()
    print('wating...')
    time.sleep(60*5)

run()

