WEB SCRAPER TO DOWNLOAD DATA FROM ALTMETRIC.COM
- timeseries data
  Date,News mentions,Blog mentions,Policy mentions,Patent mentions,Twitter mentions,Peer review mentions,Weibo mentions,Facebook mentions,Wikipedia mentions,Google+ mentions,LinkedIn mentions,Reddit mentions,Pinterest mentions,F1000 mentions,Q&A mentions,Video mentions

- mentions (in textual data)
  Mention Type,Mention Date,Outlet or Author,Mention Title,Country,External Mention ID,Mention URL,Research Output Title,Journal/Collection Title,Authors at my Institution,Departments,Output Type,Subjects (FoR),Affiliations (GRID),Publication Date,Altmetric Attention Score,Details Page URL,DOI,ISBN,National Clinical Trial ID,URI,PubMed ID,PubMedCentral ID,Handle.net IDs,ADS Bibcode,arXiv ID,RePEc ID,SSRN,URN

Required:
- Valid username and password for altmetric
- Recent version of Chromedriver (current version
  is included in repository).
- Python 3.7, preferably using an Anaconda Distribution
- Run pip install selenium

Setup:
- Please enter login credentials into keys_default.json,
  and rename to keys.json.
- Please enter list of DOIs in DOIs.txt (see example)

Running instructions:
- Open terminal and type

activate (for anaconda)

python altmetric.py