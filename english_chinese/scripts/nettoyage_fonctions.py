#!usr/bin/python
#*-* encoding: utf-8*-*
import regex

def enleve_ascii(chemin, nom_fichier, nveau_nom_fichier):
	"""
		Prend un fichier en entrée et le lit ligne par ligne
		en filtrant sur les lignes qui ne sont pas ascii
		écrit les phrases en chinois dans un nouveau fichier
	"""
	with open(chemin + nom_fichier, 'r') as file_in:
			texte = file_in.readlines()
			texte = filter(lambda l: not l.isascii(), texte)
			with open(chemin + nveau_nom_fichier, 'w') as file_out:
				for l in texte:
					file_out.write(l)
	return
	
def retourne_ligne_cn(chemin, nom_fichier, nveau_nom_fichier):
	"""
		Prend un fichier de tete écrit en chinois en entrée
		le split sur le caractère de ponctuation chinois de fin de phrase : 。
		écrit chaque phrase dans un nouveau fichier au format string
		reprend le nouveau fichier pour remplacer les coupures
	"""
	with open(chemin + nom_fichier, 'r') as file_in:
			texte = file_in.read()
			texte = texte.split('。') # texte devient une liste où chaque élément est une phrase
			with open(chemin + nveau_nom_fichier, 'w') as file_out:
				for p in texte:
					file_out.write(p.strip()+'。\n')
	with open(chemin + nveau_nom_fichier, 'r') as file_in:
		texte = file_in.read()
		texte = regex.sub(r'。\n(。|”|\))', '。', texte)
	# 	texte = regex.sub(r'。\n。', '。', texte)
# 		texte = regex.sub(r'。\n”', '。”', texte)
# 		texte = regex.sub(r'。\n\)', '。\)', texte)
		return