""" 
Script to collect meta data from Altmetric
"""


# import relevant modules
import time
from selenium import webdriver
import json
import glob, os, os.path

keys=json.loads(open('keys.json').read().replace('\n',''))

import os
cwd = os.getcwd()

try:
    os.mkdir('in')
except:
    1+1
import shutil

download_dir = 'c:/Users/hdatta/downloads'
import os
cwd = os.getcwd()


def wipe():
    global download_dir
    filelist = glob.glob(os.path.join(download_dir, "altmetric*.csv"))
    for f in filelist:
        os.remove(f)


# open webdriver (needed, because rain info is only displayed when hovered over..)
def init():
    global browser
    browser = webdriver.Chrome()
    
    browser.get('https://www.altmetric.com/explorer/login')
    browser.implicitly_wait(3)

    # accept/reject cookies and other things
    email=browser.find_element_by_id('email')
    email.clear()
    email.send_keys(keys['username'])
    
    pw=browser.find_element_by_id('password')
    pw.clear()
    pw.send_keys(keys['password'])
    
    browser.find_element_by_name('commit').click()

    browser.implicitly_wait(3)
    
    
    
"""
Url: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
"""
import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]    

def get_doi(doi, type):
    global browser
    global download_dir
    
    if (type=='timeline'):
        baseurl='https://www.altmetric.com/explorer/timeline?identifier='+doi+'&scope=all'
    if (type=='mentions'):
        baseurl='https://www.altmetric.com/explorer/mentions?identifier='+doi+'&scope=all'
        
    browser.get(baseurl)
    time.sleep(1)
    
    el=browser.find_element_by_class_name('attention-export-action')
    
    url=el.get_attribute('href')
    time.sleep(.5)
    wipe()
    
    browser.get(url)
    
    time.sleep(2)
    
    filelist = glob.glob(os.path.join(download_dir, "altmetric*.csv"))
    
    
    if len(filelist)>1: raise('DOWNLOAD ERROR: multiple files detected!!!!')
    
    import re

    m = re.search('identifier=(.+?)&', baseurl)
    if m:
        found = m.group(1)
        
    shutil.move(filelist[0], 'in/'+clean_filename(type+"_"+found+'.csv'))
    
    time.sleep(1)

    
def load_dois():
    f=open('DOIs.txt').readlines()
    dois=[]
    for i in f: 
        dois.append(i.replace('\n',''))
    return(dois)

dois=load_dois()

 
init()

def timeline():
    for doi in dois:
        try:
            get_doi(doi, type='timeline')
        except:
            print('error')
            time.sleep(5)
def mentions():
    for doi in dois:
        try:
            get_doi(doi, type='mentions')
        except:
            print('error')
            time.sleep(5)
mentions()