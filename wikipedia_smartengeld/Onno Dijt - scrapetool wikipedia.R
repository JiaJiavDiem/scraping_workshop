
library(rvest)
library(magrittr)
library(SnowballC)

load(system.file("words", "dutch.RData", package = "SnowballC"))
voc <- voc[which(nchar(voc[[1]])>3), ]

urls <- c('https://nl.wikipedia.org/wiki/Diagnose',
          'https://nl.wikipedia.org/wiki/Operatie_(medisch)',
          'https://nl.wikipedia.org/wiki/Geneeskundige_terminologie',
          'https://nl.wikipedia.org/wiki/Lijst_van_aandoeningen',
          'https://nl.wikipedia.org/wiki/Lijst_van_beroepen',
          'https://nl.wikipedia.org/wiki/Categorie:Juridische_terminologie',
          'https://nl.wikipedia.org/wiki/Categorie:Economische_terminologie',
          'https://nl.wikipedia.org/wiki/Categorie:Filosofische_terminologie',
          'https://nl.wikipedia.org/w/index.php?title=Categorie:Filosofische_terminologie&pagefrom=Probleem+van+het+lijden#mw-pages',
          'https://nl.wikipedia.org/wiki/Geneesmiddel',
          'https://nl.wikipedia.org/wiki/Lijst_van_verpleegkundige_specialisaties',
          'https://nl.wikipedia.org/wiki/Lijst_van_soorten_artsen',
          'https://nl.wikipedia.org/wiki/Categorie:Medische_apparatuur',
          'https://nl.wikipedia.org/wiki/Categorie:Medisch_instrument',
          'https://nl.wikipedia.org/wiki/Geneeskunde',
          'https://nl.wikipedia.org/wiki/Chirurgie',
          'https://nl.wikipedia.org/wiki/Gynaecologie')

extract_underlying_url <- function(url){
urls_scrape <- read_html(url)%>%
  html_nodes(.,"a") %>%
  html_attr(.,"href") %>%
  .[grep('^/wiki/',.)]

urls_scrape <- urls_scrape[-grep('Wikimedia|Wiktionary|Bestand|Wikipedia|Speciaal|Portaal|Latijn|Grieks|Categorie|Hoofdpagina|Overleg|latijn', urls_scrape)]
urls_scrape[1:(length(urls_scrape)-3)]
}

all_urls <- lapply(urls, function(x){extract_underlying_url(x)}) %>% 
  unlist() %>%
  paste('https://nl.wikipedia.org',.,sep = '') %>%
  .[!duplicated(.)]

all_urls <- lapply(all_urls, function(x){extract_underlying_url(x)}) %>% 
  unlist() %>%
  paste('https://nl.wikipedia.org',.,sep = '') %>%
  .[!duplicated(.)]

extract_words <- function(url){

scraping_wiki <- read_html(url)

all_text <- scraping_wiki %>%
  html_nodes("p") %>%
  html_text()

all_text_2 <- scraping_wiki %>%
  html_nodes("ul") %>%
  html_text()

words <- all_text %>%
  gsub('\n|\r|[[:punct:]]',' ',.) %>%
  gsub('[^[:alnum:][:space:]]',' ',.) %>%
  strsplit('[[:space:]]') %>%
  sapply(., function(x){x[which(nchar(x)>1)]}) %>%
  unlist() %>%
  .[!duplicated(.)]

words_2 <- all_text_2 %>%
  gsub('\n|\r|[[:punct:]]',' ',.) %>%
  gsub('[^[:alnum:][:space:]]',' ',.) %>%
  strsplit('[[:space:]]') %>%
  sapply(., function(x){x[which(nchar(x)>1)]}) %>%
  unlist() %>%
  .[!duplicated(.)]

c(words,words_2)
}

words_final <- lapply(all_urls, function(x){print(x);extract_words(x)}) %>%
  unlist() %>%
  .[!duplicated(.)]

#words_voc <- voc$word
#length(c(words_voc , words_final))

words_total <- c(words_final)
words_total <- tolower(words_total)[!duplicated(tolower(words_total))]
words_total <- words_total[-grep("[[:digit:]]",words_total)]

save(words_total, file = 'C:/Data/Woordenlijst_nl_2dim.R')



