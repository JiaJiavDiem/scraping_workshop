import pandas as pd
import matplotlib.pyplot as plt 
import requests
from bs4 import BeautifulSoup
import os.path

#Eerst maar eens de Top2000 ophalen, deze heb ik via de website in Excel gedownload.
def download_top():
    r=requests.get('http://www.nporadio2.nl/data/download/TOP-2000-2018.xls')
    with open('TOP-2000-2018.xls', 'wb') as f:
        f.write(r.content)

def read_data():  
    global df_Top2000
    df_Top2000 = pd.read_excel('TOP-2000-2018.xls', header=None)
    df_Top2000.columns = ['Postitie', 'Nummer', 'Artiest', 'Jaartal']
    df_Top2000["Songtekst"] = ""
    df_Top2000["AantalWoorden"] = 0

def describe_data():
    #Top 10 van artiesten met meeste nummers in Top 2000.
    print(df_Top2000.groupby(['Artiest']).size().reset_index(name='counts').sort_values(['counts'], ascending=False).head(10))
    
    #Grafiekje met aantal nummers per jaartal.
    df_jaartallen = df_Top2000.groupby(['Jaartal']).size().reset_index(name='counts').sort_values(['Jaartal'], ascending=True)
    ax = df_jaartallen.plot.bar(x='Jaartal', y='counts', rot=45)
    plt.show()

def collect(limit=10):
    #Door het dataframe lopen en voor ieder nummer de lyrics ophalen.
    for index, song in df_Top2000.head(limit).iterrows():
        if os.path.exists("songteksten\\" + str(song.Postitie) + ".txt"):
            text_file = open("songteksten\\" + str(song.Postitie) + ".txt", "r")
            text_file_content = text_file.read()
            df_Top2000.set_value(index,'Songtekst', text_file_content)
            df_Top2000.set_value(index,'AantalWoorden', len(text_file_content.split()))
        else:
            zoekartiestURL = "https://www.songteksten.nl/search?query=" + song.Artiest.replace(" ", "%20") + "&Zoeken=Zoeken"
            zoekartiestRequest = requests.get(zoekartiestURL)
    
            lijstsongsURL = BeautifulSoup(zoekartiestRequest.content, 'html5lib').find('table').find('a')['href']
            lijstsongsRequest = requests.get("https://www.songteksten.nl" + lijstsongsURL)
            for songlink in BeautifulSoup(lijstsongsRequest.content, 'html5lib').find('table').find_all('a'):
                for span in songlink.find_all('span'):
                    if song.Nummer in span.text:
                        songURL = songlink['href']
                        songRequest = requests.get("https://www.songteksten.nl" + songURL)
                        songText = BeautifulSoup(songRequest.content, 'html5lib').find("span", attrs = {'itemprop' : 'description'}).text
                        text_file = open("songteksten\\" + str(song.Postitie) + ".txt", "w")
                        text_file.write(songText)
                        text_file.close()
                        df_Top2000.set_value(index,'Songtekst', songText)
                        df_Top2000.set_value(index,'AantalWoorden', len(songText.split()))
    
try:
    os.mkdir('songteksten')
except:
    print('directory exists')
    
# run:
download_top()
read_data()
describe_data()
collect()


#collect(100)

#Sentiment analyse van de nummers.
df_negatief = open("sentiment/negative-words.txt",'r').read().splitlines()
df_positief = open("sentiment/positive-words.txt",'r').read().splitlines()
#Hier ben ik even gestopt, voor het huiswerk is dit wel voldoende, misschien dat ik later nog ga hobbieen.

# File name choice?