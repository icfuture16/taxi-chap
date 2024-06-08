import os
import io
from google.cloud import vision
from google.oauth2 import service_account

# Utiliser os.path.expanduser pour résoudre le chemin vers le répertoire personnel
id_file_path = os.path.expanduser('~/Desktop/taxi/id.txt')

# Lire l'ID à partir du fichier id.txt
with open(id_file_path, 'r') as id_file:
    raspberry_id = id_file.read().strip()

# Configurer les informations d'identification Google Cloud
credentials = service_account.Credentials.from_service_account_file(os.path.expanduser('~/Desktop/taxi/credentials.json'))

client = vision.ImageAnnotatorClient(credentials=credentials)

# Chemin vers l'image
image_path = os.path.expanduser(f'~/Desktop/taxi/img_prix/{raspberry_id}.png')

with io.open(image_path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

if texts:
    extracted_text = texts[0].description
else:
    extracted_text = "No text found"

# Enregistrer le texte extrait dans un fichier spécifique à l'ID
output_file = os.path.expanduser(f'~/Desktop/taxi/{raspberry_id}.txt')
with open(output_file, 'w') as f:
    f.write(extracted_text)

print(f"Text extracted and saved to {output_file}")
