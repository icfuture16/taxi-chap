import time
import os
import subprocess

# Utiliser os.path.expanduser pour résoudre le chemin vers le répertoire personnel
id_file_path = os.path.expanduser('~/Desktop/taxi/id.txt')

# Lire l'ID à partir du fichier id.txt
with open(id_file_path, 'r') as id_file:
    raspberry_id = id_file.read().strip()

# Nom du fichier de demande
request_file = os.path.expanduser(f'~/Desktop/taxi/@{raspberry_id}.txt')

# Vérifier et créer le fichier de demande s'il n'existe pas
if not os.path.exists(request_file):
    with open(request_file, 'w') as f:
        f.write('')

def check_request():
    with open(request_file, 'r+') as f:
        content = f.read().strip()
        if content == "prix_client":
            # Vider le fichier
            f.seek(0)
            f.truncate()
            return True
    return False

while True:
    if check_request():
        # Lancer le script d'extraction et d'envoi
        subprocess.run(["python3", os.path.expanduser("~/Desktop/taxi/extract_and_update.py")])
        subprocess.run(["/bin/bash", os.path.expanduser("~/Desktop/taxi/upload_to_github.sh")])
    
    # Attendre avant de vérifier à nouveau
    time.sleep(5)
