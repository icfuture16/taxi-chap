import subprocess
import cv2
import time

# Lire l'ID depuis le fichier id.txt
with open('id.txt', 'r') as file:
    machine_id = file.read().strip()

# Commande pour prendre la photo avec libcamera-jpeg en mode sombre
commande = "libcamera-jpeg -o image.jpg -t 500 --ev -3"
subprocess.run(commande, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Charger l'image capturée avec OpenCV
image = cv2.imread("./image.jpg")

# Définir une ROI limitée à la partie supérieure de l'image
height, width = image.shape[:2]
crop_percentage_top = 0.05  # 1% à rogner en haut
crop_percentage_lr = 0.05  # Compteur Centrodyne à rogner à gauche et à droite

crop_height_top = int(height * crop_percentage_top)
crop_height_bottom = int(height / 2.6)  # Compteur Centrodyne
roi = image[crop_height_top:crop_height_bottom, int(width * crop_percentage_lr):int(width * (1 - crop_percentage_lr))]

# Convertir l'image en niveaux de gris
gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Ajuster le contraste de l'image Centrodyne
alpha = 3  # Contraste 3
beta = 0   # Luminosité 0
adjusted_gray_roi = cv2.convertScaleAbs(gray_roi, alpha=alpha, beta=beta)

# Inversion de l'image
inverted_roi = cv2.bitwise_not(adjusted_gray_roi)

# Sauvegarder l'image inversée avec l'ID de la machine
image_path = f"./taxi-chap/img_prix/{machine_id}.png"
cv2.imwrite(image_path, inverted_roi)
time.sleep(1)

# Mettre à jour la branche locale en utilisant la stratégie de merge
subprocess.run("git pull origin main --no-rebase", shell=True, cwd="./taxi-chap")

# Ajouter l'image au dépôt git
subprocess.run(f"git add img_prix/{machine_id}.png", shell=True, cwd="./taxi-chap")
subprocess.run(f'git commit -m "Image du prix avec ID {machine_id}"', shell=True, cwd="./taxi-chap")

# Pousser les modifications vers GitHub
subprocess.run("git push origin main", shell=True, cwd="./taxi-chap")
