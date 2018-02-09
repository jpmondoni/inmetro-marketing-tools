## 2018 - Jp Mondoni - get email list from INMETRO website using Beautiful Soup ##
## Simple algorithm to find e-mails from INMETRO website based on company pages ##
## It is setup with RBLE certified URLs, but could be anything					##	
## The list will be further used as a marketing tool 							## 

from lxml import html
import requests, re, sys, os, time, csv, string
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
		soup = BeautifulSoup(page.text, "lxml")
		for link in soup.findAll('a', attrs={'href': re.compile("^detalhe_laboratorio\.asp\?nom_apelido=")}): # Regex with aimed link
			acqLink = str(link.get('href'))
			#print(acqLink)
			labList.append(acqLink)
	print('[' + time.strftime("%H:%M:%S") + ']>: Discovered ' + str(len(labList)) + ' laboratories web pages.')
	getLabContact(labList)



def getLabContact(acqList):
	
	# número de acreditação, nome do laboratório, situação, gerente, área e estado.
	i = 0
	print('[' + time.strftime("%H:%M:%S") + ']>: Acquiring prospect company contact information')
	for i in range(len(acqList)):
	#for i in range(1):
		url = ('http://www.inmetro.gov.br/laboratorios/rble/' + labList[i])
		page = requests.get(url)
		soup = BeautifulSoup(page.text, "lxml")
		for link in soup.findAll('a', attrs={'href': re.compile("^mailto:")}):
			acqMail = str(link.get('href'))	
		
		# get "Número acreditação"
		acreds = soup.find_all(lambda tag: tag.name == "td" and "Número da Acreditação " in tag.get_text())
		acreds = acreds[2:]
		for acred in acreds:
			num_acred = acred.find_next('td').get_text()
			num_acred = normalize_string(num_acred)

		# get Nome laboratório
		nomes = soup.find_all(lambda tag: tag.name == "td" and "Laboratório" in tag.get_text())
		nomes = nomes[6:7]
		for nome in nomes:
			nome_lab = nome.find_next('td').get_text()
			nome_lab = normalize_string(nome_lab)

		# get Situação 
		situacoes = soup.find_all(lambda tag: tag.name == "td" and "Situação" in tag.get_text())
		situacoes = situacoes[2:3]
		for situacao in situacoes:
			situacao_lab = situacao.find_next('td').get_text()
			situacao_lab = normalize_string(situacao_lab)

		# get Gerente
		gerentes = soup.find_all(lambda tag: tag.name == "td" and "Gerente Técnico" in tag.get_text())
		gerentes = gerentes[2:3]
		for gerente in gerentes:
			nome_gerente = gerente.find_next('td').get_text()
			nome_gerente = normalize_string(nome_gerente)

		# get UF
		ufs = soup.find_all(lambda tag: tag.name == "td" and "UF" in tag.get_text())
		ufs = ufs[2:3]
		for uf in ufs:
			sigla_uf = uf.find_next('td').get_text()
			sigla_uf = normalize_string(sigla_uf)

		contactInfo.append([acqMail[7:], num_acred, nome_lab, situacao_lab, nome_gerente, sigla_uf,  url]) # Write info on list
		print(contactInfo)
		i=i+1
	print('[' + time.strftime("%H:%M:%S") + ']>: Discovered ' + str(len(contactInfo)) + ' contacts.')
	generateCSV(contactInfo)


def generateCSV(prospectList):
	print('[' + time.strftime("%H:%M:%S") + ']>: Writing csv file with company URL page and E-mail contact')
#	with open('newcsv.csv', 'a') as labsCSV: # Append mode
	with open('newcsv.csv', 'w') as labsCSV: # Write mode

		for i in range(len(prospectList)-1):
			wr = csv.writer(labsCSV, quoting=csv.QUOTE_ALL)
			wr.writerow(prospectList[i])
	print('[' + time.strftime("%H:%M:%S") + ']>: Finished writings csv file. Total of ' + str(len(prospectList)) + ' rows were written.')


# Remove whitespaces, tabs, linebreaks and captalize string initials
def normalize_string(text):
	text = text.replace("\n", "")
	text = text.replace("\t", "")
	text = text.strip()
	if(len(text) != 2):
		text = string.capwords(text)
	return text



baseURL = 'http://www.inmetro.gov.br/laboratorios/rble/lista_laboratorios.asp?sigLab=&ordem=&tituloLab=&uf=&pais=&descr_escopo=&classe_ensaio=&area_atividade=&ind_tipo_busca=&pagina='
## Alternate version using txt file with pre-defined URLs
#with open('Pages.txt', encoding='utf-8') as file:
#	rowlist = file.readlines()
#	rowlist = [x.strip() for x in rowlist]
#	#print(rowlist)

## NOTE: Some websites may block consecutive connection requests. Be careful to don't block your IP due to high number of connections. 
for x in range(0,56):
	pageURL = baseURL+str(x)
	rowlist.append(pageURL)

getHrefFromUrl(rowlist)



