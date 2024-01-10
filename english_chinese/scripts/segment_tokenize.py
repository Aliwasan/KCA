from glob import glob
import os
import regex
import spacy
import zh_core_web_sm
import en_core_web_sm
from tqdm import tqdm
import tensorflow_hub as hub
import numpy as np
import tensorflow_text
from align import alignement

def segmentation_phrases_zh(fichier):
	"""
		param : un fichier texte en chinois
		split le texte sur les points de fin de phrases "。"
		retourne une liste de chaînes, une chaîne par phrase.
	"""
	liste_phrases =[]
	with open(fichier, 'r', encoding='utf-8') as f:
		texte = f.read()
		texte = texte.split("。")
		for l in texte:
			l = l.strip() # retrait des retours à la ligne en début ou en fin de chaine
			l = l+'。\n'
			liste_phrases.append(l)
	# on retire les retours à la ligne isolés
	for i, e in enumerate(liste_phrases):
		if e == '。\n':
			liste_phrases.pop(i)
	print(len(liste_phrases))
	print(liste_phrases)
	return liste_phrases
	
def segmentation_phrases_en(fichier):
	"""
		param : un fichier texte en anglais
		split le texte sur les points de fin de phrases "."
		retourne une liste de chaînes, une chaîne par phrase.
	"""
	liste_phrases =[]
	with open(fichier, encoding='utf-8') as f:
		texte = f.read()
		texte = regex.split(r'(?<=[a-z0-9”\)])\. |\n', texte)
		for l in texte:
			l = l.strip() # retrait des retours à la ligne ou espaces en début ou en fin de chaine
			l = l+'.\n'
			liste_phrases.append(l)
	# on retire les retours à la ligne isolés
	for i, e in enumerate(liste_phrases):
		if e == '.\n':
			liste_phrases.pop(i)
	print(len(liste_phrases))
	print(liste_phrases)
	return liste_phrases

def tokenize_zh(liste_phrases):
	""" 
		Installer le modèle spacy pour le chinois : python3 -m spacy download zh_core_web_sm
		param : une liste de chaînes de caractères en chinois : une par phrase
		Tokenise la chaîne de caractères.
		return : une liste de liste chaque liste contenant la chaîne de caractères tokenisée.
	"""
	nlp = spacy.load("zh_core_web_sm")
	nlp = zh_core_web_sm.load()
	liste_chaines = []
	for p in tqdm(liste_phrases):
		spacy_doc = nlp(p)
		chaine = [e.text for e in spacy_doc]
		liste_chaines.append(chaine)
	print(liste_chaines)
	return chaine
	
def tokenize_en(liste_phrases):
	""" 
		Installer le modèle spacy pour l'anglais' : python3 -m spacy download en_core_web_sm
		param : une liste de chaînes de caractères en anglais : une par phrase
		Tokenise la chaîne de caractères.
		return : une liste de liste chaque liste contenant la chaîne de caractères tokenisée.
	"""
	nlp = spacy.load("en_core_web_sm")
	nlp = en_core_web_sm.load()
	liste_chaines = []
	for p in tqdm(liste_phrases):
		spacy_doc = nlp(p)
		chaine = [e.text for e in spacy_doc]
		liste_chaines.append(chaine)
	print(liste_chaines)
	return liste_chaines
	
if __name__ == "__main__":

	chemin_rep_en = "../generaliste/EN/"
	chemin_rep_zh = "../generaliste/ZH/"

	
	files_EN = sorted(glob(chemin_rep_en + '*.txt'))
	files_ZN = sorted(glob(chemin_rep_zh + '*.txt'))
	
	for f in files_EN:
		liste_phrases_en = segmentation_phrases_en(f)
		tokenised_doc_en = tokenize_en(liste_phrases_en)
	
	for f in tqdm(files_ZH):
		liste_phrases_zh = segmentation_phrases_zh(f)
		tokenised_doc_zh = tokenize_zh(liste_phrases_zh)