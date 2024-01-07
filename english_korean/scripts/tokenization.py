#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spacy
from konlpy.tag import Mecab

def tokenize_english(input_file, output_file):
    """
    Tokenise les phrases en anglais à l'aide du modèle SpaCy.

    Parameter:
    - input_file (str): Chemin du fichier d'entrée contenant les phrases en anglais.
    - output_file (str): Chemin du fichier de sortie où seront sauvegardés les tokens.
    """

    # Charger le modèle SpaCy
    nlp = spacy.load("en_core_web_sm")

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Tokenisation de la phrase en anglais
            tokens = [token.text for token in nlp(line.strip())]

            # Écrit chaque token sur une nouvelle ligne dans le fichier de sortie
            for token in tokens:
                outfile.write(token + '\n')


def tokenize_korean(input_file, output_file):
    """
    Tokenise les phrases en coréen à l'aide du tokenizer Mecab.

    Parameters:
    - input_file (str): Chemin du fichier d'entrée contenant les phrases en coréen.
    - output_file (str): Chemin du fichier de sortie où seront sauvegardés les tokens.

    Returns:
    - None
    """

    # Créé une instance du tokenizer Mecab pour le coréen
    mecab = Mecab()

    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            # Tokenisation de la phrase en coréen
            tokens = mecab.morphs(line.strip())

            # Écrit chaque token sur une nouvelle ligne dans le fichier de sortie
            for token in tokens:
                outfile.write(token + '\n')
                
                
if __name__ == "__main__":

	tokenize_english('spe_resultat_en.txt', 'spe_token_en.txt')
	
	tokenize_korean('spe_resultat_ko.txt', 'spe_token_ko.txt')
           
