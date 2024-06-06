import os
import requests
from flask import Flask, request, jsonify, render_template_string
from google.cloud import vision
from google.oauth2 import service_account

app = Flask(__name__)

# Chemin vers le fichier JSON des informations d'identification
credentials = service_account.Credentials.from_service_account_info(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

client = vision.ImageAnnotatorClient(credentials=credentials)

# Variable globale pour stocker les résultats de l'analyse
analysis_results = []

@app.route('/webhook', methods=['POST'])
def github_webhook():
    global analysis_results
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

                    # Enregistrer les résultats dans la variable globale
                    analysis_results = [label.description for label in labels]

                    return jsonify({'status': 'image processed'}), 200
    return jsonify({'status': 'ignored'}), 200

@app.route('/results', methods=['GET'])
def show_results():
    global analysis_results
    return render_template_string('''
        <h1>Résultats de l'Analyse d'Image</h1>
        <ul>
        {% for result in results %}
            <li>{{ result }}</li>
        {% endfor %}
        </ul>
    ''', results=analysis_results)

if __name__ == '__main__':
    app.run(debug=True)
