## 2017 - Jp Mondoni - get email list from INMETRO website using Beautiful Soup ##
## Simple algorithm to find e-mails from INMETRO website based on company pages ##
## It is setup with RBLE certified URLs, but could be anything					##	
## The list will be further used as a marketing tool 							## 

from lxml import html
import requests, re, sys, os, time, csv
from bs4 import BeautifulSoup

labList = []
contactInfo = []
rowlist = []

## This Function visits each URL on the list and get every href tag.
## The labList[] will further be used to get the lab contact.
def getHrefFromUrl(pages):
	print('[' + time.strftime("%H:%M:%S") + ']>: Searching for INMETRO labs pages urls')
	for i in range(len(pages)):
		page = requests.get(pages[i])
		soup = BeautifulSoup(page.text)
		for link in soup.findAll('a', attrs={'href': re.compile("^detalhe_laboratorio\.asp\?nom_apelido=")}): # Regex with aimed link
			acqLink = str(link.get('href'))
			#print(acqLink)
			labList.append(acqLink)
	print('[' + time.strftime("%H:%M:%S") + ']>: Discovered ' + str(len(labList)) + ' laboratories web pages.')
	getLabContact(labList)



def getLabContact(acqList):
	i = 0
	print('[' + time.strftime("%H:%M:%S") + ']>: Acquiring prospect company contact information')
	for i in range(len(acqList)):
		url = ('http://www.inmetro.gov.br/laboratorios/rble/' + labList[i])
		page = requests.get(url)
		soup = BeautifulSoup(page.text)
		for link in soup.findAll('a', attrs={'href': re.compile("^mailto:")}):
			acqMail = str(link.get('href'))
			contactInfo.append([acqMail[7:], url]) ## Append URL and Email. Also cut "mailto:" out of address
		#print(contactInfo[i])
		i=i+1
	print('[' + time.strftime("%H:%M:%S") + ']>: Discovered ' + str(len(contactInfo)) + ' contacts.')
	generateCSV(contactInfo)


def generateCSV(prospectList):
	print('[' + time.strftime("%H:%M:%S") + ']>: Writing csv file with company URL page and E-mail contact')
	with open('newcsv.csv', 'a') as labsCSV: # Append mode
#	with open('newcsv.csv', 'w') as labsCSV: # Write mode

		for i in range(len(prospectList)-1):
			wr = csv.writer(labsCSV, quoting=csv.QUOTE_ALL)
			wr.writerow(prospectList[i])
	print('[' + time.strftime("%H:%M:%S") + ']>: Finished writings csv file. Total of ' + str(len(prospectList)) + ' rows were written.')



baseURL = 'http://www.inmetro.gov.br/laboratorios/rble/lista_laboratorios.asp?sigLab=&ordem=&tituloLab=&uf=&pais=&descr_escopo=&classe_ensaio=&area_atividade=&ind_tipo_busca=&pagina='
## Alternate version using txt file with pre-defined URLs
#with open('Pages.txt', encoding='utf-8') as file:
#	rowlist = file.readlines()
#	rowlist = [x.strip() for x in rowlist]
#	#print(rowlist)

## NOTE: Some websites may block consecutive connection requests. Be careful to don't block your IP due to high number of connections. 
for x in range(45,56):
	pageURL = baseURL+str(x)
	rowlist.append(pageURL)

getHrefFromUrl(rowlist)



