## 2017 - Jp Mondoni - get email list from INMETRO website using Beautiful Soup ##
## Simple algorithm to find e-mails from INMETRO website based on company pages ##
## It is setup with RBC certified URLs, but could be anything					##	
## The list will be further used as a marketing tool 							## 

from lxml import html
import requests, re, sys, os, time, csv, string
import urllib
from bs4 import BeautifulSoup

labUrlList = []
contactList = []
rowlist = []

## This Function visits each URL on the list and get every href tag.
## The labUrlList[] will further be used to get the lab contact.
def getHrefFromUrl(pages):
	print('[' + time.strftime("%H:%M:%S") + ']>: Searching for INMETRO labs pages urls')
	aux = ''
	for i in range(len(pages)):
		href_page = requests.get(pages[i])
		href_soup = BeautifulSoup(href_page.text, "lxml")
		y = 0
		for link in href_soup.findAll('a', attrs={'href': re.compile("^detalhe_laboratorio\.asp\?num_certificado=")}): # Regex with aimed link
			y = y + 1
			if y % 2 == 0: 
				labUrl = str(link.get('href'))
				labUrl = urllib.parse.quote(labUrl, safe=';/?:@&=+$,', encoding='windows-1252')
				labUrlList.append(labUrl)

	print('[' + time.strftime("%H:%M:%S") + ']>: Discovered ' + str(len(labUrlList)) + ' laboratories web pages.')
	getLabContact(labUrlList)



def getLabContact(getList):
	contactList = []
	contactInfo = []

	print('[' + time.strftime("%H:%M:%S") + ']>: Fetching prospect company contact information')
	for i in range(len(getList)):
		url = ('http://www.inmetro.gov.br/laboratorios/rbc/' + labUrlList[i])
		page = requests.get(url)
		page.encoding = 'windows-1252'
		soup = BeautifulSoup(page.text, "lxml")
		# get Manager Name ----------
		x = 0
		tds = soup.find_all(lambda tag: tag.name == "td" and "Gerente" in tag.get_text())
		for td in tds:
			Manager = td.find_next('td').get_text()
			contactInfo.insert(x, Manager)
			x=x+1
		Manager = contactInfo[2]
		Manager = Manager.replace('\n','')
		Manager = Manager.replace('\t','')
		Manager = Manager.strip()
		Manager = string.capwords(Manager)

		# get Email -----------------
		for link in soup.findAll('a', attrs={'href': re.compile("^mailto:")}):
			Mail = str(link.get('href'))
			Mail = Mail.replace(",", ";")

		# get Area ------------------
		y = 0
		areas = soup.find_all(lambda tag: tag.name == "td" and "Grupo de Serv" in tag.get_text())
		for f in areas:
			Area = f.find_next('td').get_text()
			Area = string.capwords(Area)

		# insert found values into list
		contactList.append([Manager, Area, Mail[7:], url])
		Manager = ''
		Area = '' 
		Mail = ''
		url = ''
		i=i+1
		generateCSV(contactList)
		del contactList[:]
	print('[' + time.strftime("%H:%M:%S") + ']>: Finished writing to csv file. A total of ' + str(i) + ' rows were written.')


def generateCSV(prospectList):
	with open('rbc.csv', 'a') as labsCSV: # Append mode

		for i in range(len(prospectList)):
			wr = csv.writer(labsCSV, quoting=csv.QUOTE_ALL)
			wr.writerow(prospectList[i])

## Alternate version using txt file with pre-defined URLs
#with open('Pages.txt', encoding='utf-8') as file:
#	rowlist = file.readlines()
#	rowlist = [x.strip() for x in rowlist]
#	#print(rowlist)

## NOTE: Some websites may block consecutive connection requests. Be careful to don't block your IP due to high number of connections. 
baseURL = 'http://www.inmetro.gov.br/laboratorios/rbc/lista_laboratorios.asp?descr_ordem=num_certificado&nom_servico=&descr_area_atuacao=&nom_laboratorio=&sig_uf=&ind_pagina='
for x in range(0,95):
	pageURL = baseURL+str(x)
	rowlist.append(pageURL)
	#print(pageURL)

getHrefFromUrl(rowlist)