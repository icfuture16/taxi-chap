import os
import requests
from flask import Flask, request, jsonify
from google.cloud import vision
from google.oauth2 import service_account

app = Flask(__name__)

# Chemin vers le fichier JSON des informations d'identification
credentials = service_account.Credentials.from_service_account_file(
    '/home/hlab/Desktop/taxi/credentials.json')

client = vision.ImageAnnotatorClient(credentials=credentials)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    # Vérifiez que l'événement est un push
    if data['ref'] == 'refs/heads/main':
        # Récupérer le fichier modifié
        for commit in data['commits']:
            for file in commit['modified']:
                if 'img_prix/' in file:
                    # Télécharger l'image depuis GitHub
                    image_url = f"https://raw.githubusercontent.com/{data['repository']['full_name']}/main/{file}"
                    response = requests.get(image_url)
                    image_content = response.content

                    # Envoyer l'image à l'API Cloud Vision
                    image = vision.Image(content=image_content)
                    response = client.label_detection(image=image)
                    labels = response.label_annotations

                    # Afficher les résultats
                    print('Labels:')
                    for label in labels:
                        print(label.description)

                    return jsonify({'status': 'image processed'}), 200
    return jsonify({'status': 'ignored'}), 200

if __name__ == '__main__':
    app.run(debug=True)
