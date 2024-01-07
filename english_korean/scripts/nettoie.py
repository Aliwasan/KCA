#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def supp(nom_fichier):
    """
    Supprime des lignes ou début de lignes en fonction de motifs spécifiques aux corpus
    
    Parameters:
    - nom_fichier (str): Le nom du fichier à traiter.
    """
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    # Supprime les débuts de lignes commençant par des motifs tels que 1.1, 1-1, 1-1. , 1., 1), 1 , I*., **, -, _
    supp_debut = re.compile(r'^(\b\d[\d,.-]*[)]?)|([*?])|([\u2160-\u2162]+)|([(][a-zA-Z]+[)])|([-,_])')

    # Supprime les débuts de lignes correspondant au motif
    lignes_filtrees_debut = [supp_debut.sub('', ligne) for ligne in lignes]

    # Supprime les occurrences des symboles spécifiés peu importe leur position dans le texte
    supp_symbole = re.compile(r'[※,▲,#*,Î,¿,ø,¹,®,À,»,Á,¦,°,Ç,Ï,ö,¾,Ê,½,´,Ù,º,±,â,ç,Â,µ,û,Ñ,Û]')

    lignes_filtrees = [supp_symbole.sub('', ligne) for ligne in lignes_filtrees_debut]

    with open(nom_fichier, 'w') as fichier:
        fichier.writelines(lignes_filtrees)

        
def supp_urls_mails(nom_fichier):
    """
    Supprime les adresses mail, les urls, et les parenthèses vides d'un fichier.
    
    Parameters:
    - nom_fichier (str): Le nom du fichier à traiter.
    """
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    lignes_filtrees = []
    for ligne in lignes:
        # Supprime les adresses mail
        ligne_sans_email = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', ligne)

        # Supprime les urls dans des phrases
        ligne_sans_urls = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))\s*', '', ligne_sans_email)

        # Supprime les parenthèses vides restantes --> notamment quand les adresses mails/urls étaient entre parenthèses
        ligne_sans_parentheses_vides = re.sub(r'\(\s*\)', '', ligne_sans_urls)

        lignes_filtrees.append(ligne_sans_parentheses_vides.strip())

    with open(nom_fichier, 'w') as fichier:
        fichier.write('\n'.join(lignes_filtrees))

if __name__ == "__main__":

    nom_fichier = 'test_en.txt'

    supp_urls_mails(nom_fichier)

    supp(nom_fichier)


# sed -i 's/^[ \t]*//' gen_resultat_en.txt --> sert à retirer les espaces en trop en début de ligne
# sed -i '/^$/d' gen_resultat_en.txt --> sert à retirer les lignes vides
# sed -i 's/^\.//' gen_resultat_en.txt  --> supprime les points en début de phrase suite à la suppression des chiffres romains qui étaient suivis d'un point. 
# -> ma regex initial voulait aussi supprimer les points que ça me supprimait aussi les ponctuations de fin de phrases, et peut importe les tentatives je n'ai pas réussi à changer cela.
