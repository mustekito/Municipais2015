##!/usr/bin/env python
# -*- coding: utf-8 -*-
#Autor: Álvaro Ordóñez
#Instruccións: Completar as liñas que están comentados.

from bs4 import BeautifulSoup
import requests,tweepy

ficheiro = open('/home/???/escru.txt', 'r+') #Onde se garda o valor do anterior escrutinio
porcentaxe=ficheiro.readline().strip()

url="http://resultadoslocales2015.interior.es/?????????????????????" #Web de Interior co concello que queremos publicar
auth = tweepy.OAuthHandler("API Key", "API Secret") #API Keys de Twitter
auth.set_access_token("Token", "Token-Secret") #Tokens de Twitter
api = tweepy.API(auth)

tweet=""
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data)

escrutado=soup.find("div", {"id": "xescrutado"})
for span in escrutado.find_all('span', recursive=False):
	porcentaxeNova=span.string.strip()
	tweet=tweet+"Escrutado " + porcentaxeNova + "\n"
if(porcentaxe!=porcentaxeNova):
	porcentaxe=porcentaxeNova;
	ficheiro.seek(0); ficheiro.write(porcentaxeNova);
	table=soup.find(id="TVRESULTADOS")

	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	for row in rows:
		partido=row.findAll('th')[0].string.strip()
		cols=row.findAll('td')
		concelleiros=cols[3].string.strip()
		if(concelleiros!=""):
			tweet=tweet+partido + " " + concelleiros  + "\n"
	tweet=tweet+"#SantiagoDeCompostela"
	print tweet
	api.update_status(status=tweet)
		
ficheiro.close()
