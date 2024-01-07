#!/bin/bash

# Installation outils au préalable : https://pyhwp.readthedocs.io/en/latest/converters.html#requirements
# Pour la commande utilisée : https://pyhwp.readthedocs.io/en/latest/converters.html#hwp5txt-text-conversion


# Chemin du dossier contenant les fichiers HWP
dossier_hwp="/home/camille/Downloads/02_말뭉치/병렬/한영병렬/한영병렬_말뭉치/원시_말뭉치/원시_말뭉치/"

# Chemin du fichier journal d'erreur
fichier_journal="/home/camille/Downloads/log_conversion.txt"

cd "$dossier_hwp" || exit

# Initialise le journal
echo "Journal de conversion HWP" > "$fichier_journal"
echo "--------------------------" >> "$fichier_journal"

# Boucle sur tous les fichiers HWP dans le dossier
for fichier_hwp in *.hwp; do
    # Vérifie si le fichier HWP existe
    if [ -e "$fichier_hwp" ]; then
        # Extrait le nom fichier
        nom_base=$(basename "$fichier_hwp" .hwp)

        # Utilise la commande hwp5txt pour convertir le fichier HWP en texte
        if hwp5txt --output "${nom_base}.txt" "$fichier_hwp" 2>> "$fichier_journal"; then
            echo "Conversion réussie : $fichier_hwp -> ${nom_base}.txt"
        else
            # Enregistre le nom du fichier qui n'a pu être converti dans le journal
            echo "Échec de la conversion : $fichier_hwp" >> "$fichier_journal"
        fi
    else
        # Enregistre le nom du fichier non trouvé dans le journal
        echo "Le fichier $fichier_hwp n'existe pas." >> "$fichier_journal"
    fi
done
