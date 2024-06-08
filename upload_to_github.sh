#!/bin/bash

# Lire l'ID à partir du fichier id.txt
id=$(cat ~/Desktop/taxi/id.txt)

# Naviguer vers le répertoire contenant le fichier id.txt
cd ~/Desktop/taxi

# Ajouter et valider les modifications
git add ${id}.txt
git commit -m "Updated price for Raspberry Pi ${id}"

# Pousser les modifications vers GitHub
git push origin main
