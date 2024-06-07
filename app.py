import os
import requests
from flask import Flask, request, jsonify, render_template_string
from google.cloud import vision
from google.oauth2 import service_account

app = Flask(__name__)

# Initialiser les informations d'identification Google Cloud Vision
credentials = service_account.Credentials.from_service_account_file('/home/hlab/Desktop/taxi/credentials.json')
client = vision.ImageAnnotatorClient(credentials=credentials)

# Variable globale pour stocker les résultats
results = []

@app.route('/webhook', methods=['POST'])
def github_webhook():
    global results
    data = request.json
    if data['ref'] == 'refs/heads/main':
        for commit in data['commits']:
            for file in commit['modified']:
                if 'img_prix/' in file:
                    image_url = f"https://raw.githubusercontent.com/{data['repository']['full_name']}/main/{file}"
                    response = requests.get(image_url)
                    image_content = response.content

                    # Envoyer l'image à Google Cloud Vision pour analyse
                    image = vision.Image(content=image_content)
                    response = client.label_detection(image=image)
                    labels = response.label_annotations

                    # Stocker les résultats dans la variable globale
                    results = [label.description for label in labels]

                    return jsonify({'status': 'image processed'}), 200
    return jsonify({'status': 'ignored'}), 200

@app.route('/results', methods=['GET'])
def show_results():
    global results
    # Afficher les résultats dans une page web
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Cloud Vision Results</title>
      </head>
      <body>
        <div class="container">
          <h1 class="mt-5">Cloud Vision Results</h1>
          <ul class="list-group">
            {% for result in results %}
              <li class="list-group-item">{{ result }}</li>
            {% endfor %}
          </ul>
        </div>
      </body>
    </html>
    ''', results=results)

if __name__ == '__main__':
    app.run(debug=True)
