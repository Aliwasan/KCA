#!usr/bin/python
#*-* encoding: utf-8*-*
from nettoyage_fonctions import enleve_ascii, retourne_ligne_cn

chemin = './generaliste/'
nom_fichier = "ZH_1.txt"
nveau_nom_fichier1 = "ZH_1_uniq_cn.txt"
nveau_nom_fichier2 = "ZH_1_retour_ligne.txt"

enleve_ascii(chemin, nom_fichier, nveau_nom_fichier1)

retourne_ligne_cn(chemin, nveau_nom_fichier1, nveau_nom_fichier2)


