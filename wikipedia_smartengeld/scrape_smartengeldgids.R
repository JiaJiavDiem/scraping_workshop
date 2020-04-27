
library(httr)
library(RSelenium)
library(rvest)

# https://stackoverflow.com/questions/45395849/cant-execute-rsdriver-connection-refused
# https://stackoverflow.com/questions/46028200/rselenium-connection-refused-error/51885152#51885152

shell('docker run -d -p 4444 selenium/standalone-chrome')
#shell('docker run --help')

url <- 'https://www.smartengeld.nl'

driver <- rsDriver(port = 4444L,browser=c("chrome"), chromever="74.0.3729.6")
remote_driver <- driver[["client"]]
remote_driver$open()
remote_driver$navigate(url)

name_element <- remote_driver$findElement(using = 'css selector', value = '#edit-name')
name_element$sendKeysToElement(list("info@medirisk.nl"))

name_element <- remote_driver$findElement(using = 'css selector', value = '#edit-pass')
name_element$sendKeysToElement(list("TeamMR"))

remote_driver$findElement(using = 'css selector', value = "#edit-submit--2")$clickElement()

remote_driver$navigate('https://www.smartengeld.nl/search/site/')
remote_driver$findElement(using = 'css selector', value = '#facetapi-link--244')$clickElement()

# Selecteren van cases:

#Pagina format: https://www.smartengeld.nl/search/site?page=15&f%5B0%5D=im_field_hoofdcategorie%3A337
extract_text <- function(page = NULL){
  Sys.sleep(sample(10:40,1))     # randomizen van delay 
  if(is.null(page)){
    remote_driver$navigate('https://www.smartengeld.nl/search/site?f%5B0%5D=im_field_hoofdcategorie%3A337')
    headers <- remote_driver$findElement(using = 'css selector', value = "#block-system-main")$getElementText()
    headers
  } else {
    remote_driver$navigate(paste('https://www.smartengeld.nl/search/site?page=',page,'&f%5B0%5D=im_field_hoofdcategorie%3A337', sep = ''))
    headers <- remote_driver$findElement(using = 'css selector', value = "#block-system-main")$getElementText()
    headers
  }
}

lists_pages_text <- c(unlist(extract_text()), unlist(lapply(1:15, function(x){extract_text(x)})))

# Case wegzetten in Header --> Body

extract_paginas <- function(text){
  text_split <- strsplit(text, '\n')
  text_relevant <- as.character(sapply(text_split, function(x){x[grep('^[[:digit:]]{3}',x)]}))
  text_relevant <- gsub('\\|','',text_relevant)
  text_relevant_subsplit <- strsplit(text_relevant, '[[:space:]]')
  text_relevant_subsplit <- sapply(text_relevant_subsplit, function(x){x[nchar(x)>0]})
  lapply(text_relevant_subsplit, function(x){paste(x[1:(length(x)-2)], collapse = '-')})
}

pagina <- unlist(lapply(lists_pages_text, function(x){extract_paginas(x)}))
pagina <- gsub('-in-','-',pagina)
pagina <- gsub('\\(|\\)|\\/','',pagina)

# Vaste velden ophalen
scrape_data <- function(pagina){
  Sys.sleep(sample(10:40,1))                               #randomizen van delay
remote_driver$navigate(paste('https://www.smartengeld.nl/uitspraak/',pagina,sep = ''))
text_fout      <- remote_driver$findElement(using = 'css selector', value = '#block-uitspraak-uitspraak-ongeval')$getElementText()
text_uitspraak <- remote_driver$findElement(using = 'css selector', value = '#block-uitspraak-uitspraak-uitspraak')$getElementText()
text_totaal    <- remote_driver$findElement(using = 'css selector', value = '#main')$getElementText()
list(text_fout, text_uitspraak, text_totaal)
}

data_totaal <- lapply(pagina, function(x){scrape_data(x)})

build_database <- function(data){
  vaste_kenmerken_text     <- paste("TYPE\n", 
                                    gsub('DATUM','DATUMINCIDENT',data[[1]]),
                                    gsub('DATUM','DATUMUITSPRAAK',data[[2]]),
                                    sep = '')
  omschrijving_text        <- strsplit(data[[3]][[1]], '\n')
  vaste_kenmerken_text     <- strsplit(vaste_kenmerken_text, '\n')
  
  id_smartgids             <- as.numeric(unlist(strsplit(gsub('Home ','',data[[3]][[1]]), '[[:space:]]'))[2])
  
  testsplit <- sapply(omschrijving_text, function(x){grep('GEÏNDEXEERD BEDRAG|OORSPRONKELIJK TOEGEWEZEN BEDRAG',x)})
  testsplit_values <- c(testsplit+1,testsplit[2]+2)
  data_output_omsch  <- data.frame(id = id_smartgids,
                             kenmerk = c(sapply(omschrijving_text , function(x){x[testsplit]}),'omschrijving'),
                             values =    sapply(omschrijving_text, function(x){x[testsplit_values]}), stringsAsFactors = FALSE)
  
  data_output_vast   <- data.frame(id = id_smartgids,
                                   kenmerk = vaste_kenmerken_text[[1]][which((1:length(vaste_kenmerken_text[[1]]))%%2==1)],
                                   values = vaste_kenmerken_text[[1]][which((1:length(vaste_kenmerken_text[[1]]))%%2==0)],
                                   stringsAsFactors = FALSE)
  rbind(data_output_omsch, data_output_vast)
}

database <- lapply(1:length(data_totaal), function(x){build_database(data_totaal[[x]])})
database <- data.table::rbindlist(database)
database <- database[!duplicated(database),]
database <- tidyr::spread(database, key = 'kenmerk', value = values, fill = NA)

save(database, file = 'C:/Users/MediRisk-4/Desktop/data_smartengeld.RData')


