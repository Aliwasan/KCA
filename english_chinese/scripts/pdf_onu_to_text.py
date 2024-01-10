#!usr/bin/python
#*-* encoding: utf-8*-*

# ici on suppose que :
# - le nom des fichiers est suffixé par un C pour le chinois et un E pour l'anglais, ex : A_61_20C.pdf et A_61_20E.pdf
# - le répertoire comprend uniquement des fichiers en EN et en ZH
# on impose le n° de fichier en sortie (notamment pour faire suite aux n° des fichiers déjà dans notre corpus le cas échéant)
# le script ouvre un fichier pdf et applique les traitements :
# - de conversion au format texte
# - de nettoyage

# Requirements : pip install --upgrade pymupdf

import re
import regex
import sys, pathlib, fitz
import os
from glob import glob


liste = glob('./downloads/*.pdf')
print(liste)

paires_lang = {}
for e in liste:
	suf = e.split('.')[1][-1]
	#print(suf)
	if suf == 'E' or suf =='C':
		nom_fichier = e.split('/')[2]
		#print( nom_fichier)
		rad = nom_fichier.split('.')[0][:-1]
		#print(rad)
		if rad not in paires_lang:
			paires_lang[rad] = [nom_fichier]
		else:
			paires_lang[rad].append(nom_fichier)
	# else: # cas où pas de E ou C
# 		rad = e.split('.')[1][:-2]
# 		if rad not in paires_lang:
# 			paires_lang[rad] = [e]
# 		else:
# 			paires_lang[rad].append(e)

# Pour pouvoir ouvrir les fichiers parallèles dans chaque langue
# On garde uniquement les clés qui ont une liste de 2 valeurs
paires_lang = {k:v for k,v in paires_lang.items() if len(paires_lang[k]) == 2}
print(paires_lang)

cpteur_fichier = 83

for p in paires_lang.keys():
	print(f' p clé de paires_lang dico : {p}')
	cpteur_fichier +=1
	for f in paires_lang[p]:
		print(f"\n\non traite le fichier: {f}\n")
		with fitz.open('./downloads/'+ f) as doc:
			texte = " ".join([page.get_text() for page in doc])
		texte = re.sub(r'(\n{1,})', " ", texte)   
		# pattern : A/76/20 et  V.21-06705  chiffres facultatifs avant le V. ou après # ! : 46 V.11-83880 pas pris en compte
		texte = re.sub(r' +A\/\d{2}\/\d{2} +\d* +V\.\d{2}-\d+ +\d* +', " ", texte)
		# pattern :   A/78/20    27  23-11905    chiffres facultatifs avant ou après A/78/20, 23-11905 facultatif
		texte = re.sub(r' +\d* +A\/\d{2}\/\d{2}( +\d)* +(\d{2}-\d+ +)*', " ", texte)
		# cas : A/AC.105/C.1/L.406/Add.6  5/5 V.23-02608 à ajouter !
		# remplace chiffres mal nettoyés entre 2 phrases, ex : 与社会。   2 12. 空间与水
		texte = regex.sub(r'\p{L}\p{P}( +\d+ +)(?=\d+\. )', " ", texte)
		# remplace par ex :  and enable( __________________  5  )Official
		texte = re.sub(r' +_+ +\d* +', " ", texte)
		if f.split('.')[0][-1] == 'C' :
			print("chinois")
			# remplace tout ce qui est avant le premier segment 1.
			texte = regex.sub(r'(.+导言 *)(?=1\. )', " ", texte)
			# remplace les espaces multiples par un seul espace
			texte = re.sub(r' {2,}', " ", texte)
# 			print(f"texte : {texte}")
			with open(f"./retours_pdf_to_text/ZH_{cpteur_fichier}.txt", 'w') as file_out_ZH:
				m = re.findall("(\d{1,3}\.\s)?([^\d{1,3}\.\s].+?)(\d{1,3}\.\s)", texte)	 # ce qui est ENTRE 1 ou plusieurs chiffres suivis d'un point et d'un espace
				for e in m:
					file_out_ZH.write(e[1]+'\n')
		elif f.split('.')[0][-1] == 'E' :
			print("anglais")
			# remplace tout ce qui est avant le premier segment 1.
			texte = regex.sub(r'(.+Introduction *)(?= 1\. )', " ", texte)
			# remplace les espaces multiples par un seul espace
			texte = re.sub(r' {2,}', " ", texte)
			#print(f"texte : {texte}")
			with open(f"./retours_pdf_to_text/EN_{cpteur_fichier}.txt", 'w') as file_out_EN:
				m = re.findall("(\d{1,3}\.\s)?([^\d{1,3}\.\s].+?)(\d{1,3}\.\s)", texte)	 # ce qui est ENTRE 1 ou plusieurs chiffres suivis d'un point et d'un espace
				for e in m:
					file_out_EN.write(e[1]+'\n')