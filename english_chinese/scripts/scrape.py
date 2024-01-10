#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Accède à une page html par un url, extrait le contenu des balises recherchées
# Accède à la même page dans les langue recherchées identifiées par et extrait le contenu des mêmes balises dans ces langues.
# Écrit le résultat des extractions de contenus dans un seul fichier, les versions dans chaque langue à la suite l'une de l'autre.
import requests
import urllib.request
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import ssl


def is_valid(url):
	"""
	Vérifie si un lien internet est valide ou non. 
	"""
	parsed = urlparse(url)
	return bool(parsed.netloc) and bool(parsed.scheme)

def all_links (url):
	"""
	Retourne tous les URLs trouvés dans "url" et dans le site auquel il réfère
	param : un url d'entrée
	sortie : un ensemble des liens urls du domaine
	"""
	ssl._create_default_https_context = ssl._create_unverified_context
	urls = set() # toutes les URLs de 'url'
	# initie des ensemble de liens uniques
	internal_urls = set()
	external_urls = set()
	domain_name = urlparse(url).netloc	# nom de domaine de l'URL sans son protocole
# 	soup = BeautifulSoup(requests.get(url).content, "html.parser")
	request = urllib.request.Request(url, headers=headers)
	with urllib.request.urlopen(request) as webpage: 
		# Get the html content
		html = webpage.read()
		soup = BeautifulSoup(html, "html.parser")
		#print(f"soup : {soup}\n")

	# Création de tags pour chaque URl récupéré
	for a_tag in soup.find_all('a'):
		href = a_tag.attrs.get("href") # on accède au contenu de l'attribut href dans la balise anchor
		if href == "" or href is None: # on vérifie s'il y a quelque chose dans l'URL. Sinon, on passe
			continue
		# On joint les URLS au cas où les dits URLs récupérés sont relatifs
		href = urljoin(url, href)

		parsed_href = urlparse(href)
		#print(f"parsed_href = urlparse(href) : {parsed_href}\n")
		# On supprime les paramètres GET, fragments d'URL, etc pour évider les répétitions.
		href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
		#print(f"parsed_href.scheme + '://' + parsed_href.netloc + parsed_href.path : {href}\n")
		if not is_valid(href):
			# si URL invalide
			continue
		if href in internal_urls:
		# si déjà dans l'ensemble
			continue
		if domain_name not in href:
			# si lien extérieur au domaine
			continue
		#print(f"{MAGENTA}[*] Internal link: {href}{RESET}")
		urls.add(href)
		#print(f"Nombre d'urls : {len(urls)}")
	return urls
	
	
def get_html_from_url(url, charset='utf-8'):
	"""
	Extraction du code HTML à partir d'un simple URL.
	param : 	url -- l'url à racler
					charset -- encodage utilisé pour décoder les caractères
	sortie :	code source de la page
	"""
	headers = { 'User-agent' : 'HTML extractor (lin)' }
	request = urllib.request.Request(url, headers=headers)
	with urllib.request.urlopen(request) as f:
		html = f.read().decode(charset)
	return html

def parse_html_by_class(html, selecteur):
	"""
	Segmente et extrait des balises HTML au moyen des attributs "class".
	param :	html -- la page html
					selecteur -- le/les valeurs des class dont on recherche le contenu, syntaxe : .nom/valeur de l'attribut class visé
	sortie :	une liste avec les balises et leurs contenus visées par le sélecteur
	"""
	soup = BeautifulSoup(html, 'html.parser')
	balises = soup.select(selecteur)
	return balises
	
def parse_html_by_language(url, langue_id_list):
	"""
	Extrait le code HTML d'une page à partir d'un simple URL.
	Recherche dans la page html plusieurs id de langue et pour chacun d'eux
	Renvoie la liste des l'urls (un par langue) qui mènent aux pages écrites dans les langues recherchées
	param :	un url
					langue_id -- la liste des langues que l'on recherche à atteindre, telles qu'écrites en valeur de l'attribut "hreflang"
	sortie :	liste d'urls
	"""
	headers = { 'User-agent' : 'HTML extractor (lin)' }
	request = urllib.request.Request(url, headers=headers)
	charset='utf-8'
	list_urls_lang=[]
	with urllib.request.urlopen(request) as f:
		html = f.read()#.decode(charset)
		soup = BeautifulSoup(html, 'html.parser')
		cpteur_lang = 0
		for id_lang in langue_id_list:
			try :
				langue_tag = soup.find(hreflang = langue_id_list[cpteur_lang])
# 			except : #Trouver un moyen de conserver l'indice des urls qui ont donné une erreur (ils 'ont pas le hreflang), pour les éliminer au même indice dans la liste en fr.
				url_lang = langue_tag['href']
			except TypeError:
				url_manquant = url
				#print(f"url_manquant : {url_manquant}\n")
				return url_manquant
			list_urls_lang.append(url_lang)
			cpteur_lang += 1
	# 	print(list_urls_lang)
		return list_urls_lang


	
if __name__ == '__main__':
	"""Usage example.
	Works only when used as standalone.
	"""
	headers = { 'User-agent' : 'HTML extractor (lin)' }
	# url d'entrée
	url_entree = "https://www.safran-group.com/fr/groupe/presentation/espace"
	links = all_links(url_entree)
	#print(links)
	
	# Liste des langues recherchées : les langues ont été identifiées visuellement dans le code source de la page
	list_id_lang = ['en','zh-Hans']
	nbre_lang = len(list_id_lang) # 2
	list_urls = list(links)
	print(f"len(list_urls) : {len(list_urls)}\n")
	#print(f"list_urls : {list_urls}\n")
	
	# Liste des urls des langues recherchées
	list_tot_urls_lang = [] # on crée une liste qui va récupérer les urls par langue et par page
	list_urls_manquants = [] # on y met les url qui n'ont pas de hreflang avec langues recherchees dans leur code source
	for h in list_urls:
		resultat_url_language = parse_html_by_language(h, list_id_lang) # ici renvoie une liste avec autant d'urls que de langues dans id_lang
		if isinstance(resultat_url_language, str):
			list_urls_manquants.append(resultat_url_language)
		else :
			list_tot_urls_lang.extend(resultat_url_language)		
		
	print(f"len(list_tot_urls_lang : {len(list_tot_urls_lang)})\n")
	print(f"len(list_urls_manquants) : {len(list_urls_manquants)}\n")
	
	#print(f'list_tot_urls_lang : \t {list_tot_urls_lang} \n')
	#print(f'list_urls_manquants : \t {list_urls_manquants}\n')
 
	# Retrait des urls manquants de la liste des urls dans la langue d'entrée
	for u in list_urls_manquants:
		list_urls.remove(u)
	
	# print(f"len(list_urls) : {len(list_urls)}\n")
# 	print(f"list_urls : {list_urls}\n")
	
	# Identification des urls non valides dans la liste des urls par langues, commençant par "/"
	list_not_valid = [u for u in list_tot_urls_lang if u.startswith('/')]
	print(list_not_valid)
	
	# Récupération des indices des urls non valides dans la liste des urls par langues
	# ici on veut repérer uniquement l'indice de la première langue pour pouvoir retirer l'url correspondant dans la liste urls en fr
	idx_not_valid = [list_tot_urls_lang.index(list_not_valid[idx]) for idx in range(0, len(list_not_valid), 2)]
	print(idx_not_valid)
	
	# Retrait des urls non valides de la liste des urls par langue
	for u in list_not_valid:
		list_tot_urls_lang.remove(u)
	
	# Retrait des urls non valides de la liste des urls en français
	list_urls_to_remove = [list_urls[int(i/2)] for i in idx_not_valid]
	print(f"list_urls_to_remove : {list_urls_to_remove}\n")
	for u in list_urls_to_remove:
		list_urls.remove(u)
	
	# print(f"list_urls après nettoyage :{len(list_urls)}")
# 	print(f"list_tot_urls_lang après nettoyage :{len(list_tot_urls_lang)}")
	
	# Identification des urls qui n'ont pas de localisation/fr/ de la list des urls en fr
	list_urls_wout_fr_to_remove = [u for u in list_urls if u[28:31] != "/fr"]
	print(f"list_urls_wout_fr_to_remove pas de /fr/ : {list_urls_wout_fr_to_remove}\n")
	
	# Récupération des indices des urls qui n'ont pas de localisation/fr/ 
	idx_not_valid_2 = [list_urls.index(list_urls_wout_fr_to_remove[idx]) for idx in range(0, len(list_urls_wout_fr_to_remove))]
	print(f"idx_not_valid_2 : {idx_not_valid_2 }")
	
	# Retrait des urls sans correspondant /fr/ de la liste des urls par langue
	list_urls_to_remove_2 = [list_tot_urls_lang[i] for i in idx_not_valid_2]
	print(f"list_urls_to_remove_2 : {list_urls_to_remove_2}")
	
	# Retrait des urls sans localisation /fr/
	for u in list_urls_wout_fr_to_remove:
		list_urls.remove(u)
	
	# retrait des doublons dans la liste des urls par langue_id_list
	# using list comprehension + enumerate() to remove duplicated from list
	list_tot_urls_lang  = [i for n, i in enumerate(list_tot_urls_lang) if i not in list_tot_urls_lang [:n]]
	
#__________________________________________________________________________________________________________________ FIN NETTOYAGE
	print("APRES NETTOYAGE")
	
	print(f"len(list_urls) : {len(list_urls)}\n")
	print(f"list_urls : {list_urls}\n")
	
	print(f"len(list_tot_urls_lang) : {len(list_tot_urls_lang)}\n")
	print(f"list_tot_urls_lang : {list_tot_urls_lang}\n")
	
	# on établit la liste des contenus recherchés dans la langue de l'url d'entrée, grâce au sélecteur class
	# html = get_html_from_url(url_entree)
# 	Contenu recherché : liste des balises recherchées
# 	classes = parse_html_by_class(html, 'meta[name="description"], content, .c-spotlight-section__content')
# 	print (f"nombre de classes recherchées : {len(classes)}\n")
# 	print(f"classes[0] : {classes[0]}")
# 	print(f"type(classes[0]) : {type(classes[0])}")
# 	for classe in classes:
# 		print(classe)
# 		print(classe.get_text())
		
	# écrire dans des fichiers séparés par langue
# 	cpteur_file = 81
# 	cpteur_lang = 0
# 	cpteurd = 0
# 	cpteurf = 2
# 	list_lang = ['EN','ZH']
# 	with open(f"{list_lang[cpteur_lang]}_{cpteur_file}.txt", 'w') as f:
	with open("EN_82.txt", 'w') as f_en, open("ZH_82.txt", 'w') as f_cn:
		for i in range(0, len(list_tot_urls_lang), 2):
			cpteur_index = 0 # pour itérer sur les classes
			html = get_html_from_url(list_tot_urls_lang[i])
			classes = parse_html_by_class(html, 'meta[name="description"], content, .c-spotlight-section__content')
			for classe in classes:
				if classe.get_text() == "": # la 1ère classe est un attribut
					f_en.write(classe.get('content'))
					f_en.write('\n')
				else:
					f_en.write(classe.get_text().strip())
					f_en.write('\n')
				cpteur_index+=1
			html = get_html_from_url(list_tot_urls_lang[i+1])
			classes = parse_html_by_class(html, 'meta[name="description"], content, .c-spotlight-section__content')
			for classe in classes:
				if classe.get_text() == "": # la 1ère classe est un attribut
					f_cn.write(classe.get('content'))
					f_cn.write('\n')
				else:
					f_cn.write(classe.get_text().strip())
					f_cn.write('\n')
					
				cpteur_index+=1
			
				
# 	Dico des contenus dans toutes les langues (langue d'entrée est en)
# 	dico={}
# 	1ère étape : Remplissage du dico avec les contenus en fr
	# cpteur_ctrl = 0
# 	for url in list_urls:
# 		html = get_html_from_url(url)
# 		classes = parse_html_by_class(html, 'meta[name="description"], content, .c-spotlight-section__content')
# 		cpteur_index = 0 # pour itérer sur les classes
# 		for classe in classes:
# 			if classe.get_text() == "": # la 1ère classe est un attribut
# 				dico[f'fr_{cpteur_index}'] = classe.get('content')
# 			else:
# 				dico[f'fr_{cpteur_index}'] = classe.get_text().strip()
# 			cpteur_index+=1
# 		cpteur_ctrl+=1
# 		print(f"cpteur_ctrl : {cpteur_ctrl}\n")
# 		
# 	nb_entrees_lang = len(dico)
# 	print(f"len dico avec les entrées en fr : {nb_entrees_lang}\n")
# 	
# 
# # 2ème étape : On commence à itérer sur les urls des langues : on veut boucler sur les 2 premiers puis les 2 suivants etc.
# 	cpteur_d = 0
# 	cpteur_f = 2
# 	iter_nb = int((len(list_tot_urls_lang)/2)-1) # on retire 1 car dans le range commence à 0
# 	print(f"Nbre iterations sur liste urls par langues : {iter_nb}\n")
# 	for url in range(0, iter_nb): # va itérer autant de fois qu'il y a de paires d'urls
# 		url_paire = list_tot_urls_lang[cpteur_d:cpteur_f]
# 		print(f"Lecture de la paire d'éléments en cours : {url_paire}\n") # il va chercher dans la liste urls par langues
# 		cpteur_url_next_lang = 0 # pour aller sur l'url de la langue suivante
# 		for u in url_paire: # boucle sur la paire d'urls
# 			html_en_cours = get_html_from_url(u) # on parse l'url
# 			classes_lang = parse_html_by_class(html_en_cours, 'meta[name="description"], content, .c-spotlight-section__content')
# 			cpteur_index_suite = 0 # pour reprendre à 0 le comptage des index des entrées du dico à la suite du fr
# 			for classe in classes_lang :
# 				Remplissage du dico avec les contenus de la liste classe_lang
# 				if classe.get_text() == "": # la 1ère classe est un attribut
# 					dico[f'{list_id_lang[cpteur_url_next_lang]}_{cpteur_index_suite}'] =  classe.get('content').strip()
# 				else:
# 					dico[f'{list_id_lang[cpteur_url_next_lang]}_{cpteur_index_suite}'] = classe.get_text().strip()
# 				print(f"remplissage des contenus : {list_id_lang[cpteur_url_next_lang]}_{cpteur_index_suite}\n")
# 				cpteur_index_suite += 1
# 			cpteur_url_next_lang += 1
# 			print(f"cpteur_url_next_lang : {cpteur_url_next_lang}\n")
# 		cpteur_d+=2
# 		cpteur_f+=2
# 	print(f"dico :{dico}\n")
# 
# écriture du contenu du dico dans un fichier texte				
# On met en parallèle les entrées multilingues, en itérant avec range sur le nbre_entree_lang
# 	with open('multilingue.txt', 'w') as f:
# 		for s in range(0, nb_entrees_lang):
# # 			print(dico[f'en_{s}'], '\n', '________________', '\n')
# 			f.write('\nFR :\t'+dico[f'fr_{s}']+'\n')
# 			for s2 in range (0, nbre_lang):
# 				lang = list_id_lang[s2]
# # 				print(dico[f'{lang}_{s}'], '\n', '________________', '\n')
# 				f.write(lang+': \t'+dico[f'{lang}_{s}']+'\n')
# 
# # écriture du contenu du dico dans plusieurs fichiers textes : un par langue_id_list
# cpteur_fichier = 0
# with open('.txt', 'w') as f:
	# for k in dico.items():
# 		print(k)		