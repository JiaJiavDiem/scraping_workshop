Scraper
=======

Goal: 
- open a SQLite database, scrape a website and write the text of a website to the database. 
- My ultimate goal is to do topic modeling on the content of the websites

Method:
- the scraping is 3 layers deep: 
  1. scrape homepage, 
  2. open the links on the homepage and scrape these childpages, 
  3. open links on childpage and scrape the subsequent page 

Running instructions:
- scraper.py collects commonly used functions
- run.ipynb sets up the database and collects first set of scrapes
- step2CD.ipynb does last scraping

Input files:
- CSV file with websites URLs to be scraped

To do:
- incorporate step2CD in module and include in run.ipynb