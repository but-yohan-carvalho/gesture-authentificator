import cv2
import time
import os
import csv
import mediapipe as mp
from detector import HandDetector

# 1. Demander à l'utilisateur quel geste il souhaite enregistrer
gesture_name = input("Entrez le nom du geste à enregistrer (ex: poing, v, trois) : ").strip().lower()
if not gesture_name:
    print("Le nom du geste ne peut pas être vide.")
    exit()

csv_filename = "gestures_dataset.csv"
# 2. Fonction de normalisation des coordonnées
def normalize_landmarks(landmarks):
    # Prendre le poignet (point 0) comme point de référence (origine)
    base_x = landmarks[0].x
    base_y = landmarks[0].y
    
    # Rendre les coordonnées relatives au poignet
    relative_coords = []
    for lm in landmarks:
        relative_coords.append(lm.x - base_x)
        relative_coords.append(lm.y - base_y)
        
    # Mettre à l'échelle pour que les valeurs soient comprises entre -1.0 et 1.0
    # (indépendant de la distance entre la main et la caméra)
    max_val = max(abs(val) for val in relative_coords)
    if max_val > 0:
        relative_coords = [val / max_val for val in relative_coords]
        
    return relative_coords

def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    start_time = time.time()
    
    saved_count = 0
    print("\n--- INSTRUCTIONS ---")
    print("Placez votre main devant la caméra.")
    print("Appuyez sur la touche 'ESPACE' pour enregistrer une pose de ce geste.")
    print("Enregistrez environ 30 à 50 poses sous différents angles/distances.")
    print("Appuyez sur 'q' pour quitter et sauvegarder.\n")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        timestamp_ms = int((time.time() - start_time) * 1000)

        # Détecter la main
        landmarks = detector.detect(rgb_frame, timestamp_ms)

        # Si la main est détectée, on l'affiche en vert, sinon en rouge
        color = (0, 0, 255) # Rouge par défaut
        if landmarks:
            color = (0, 255, 0) # Vert si détecté
            
            # Dessiner le point du poignet et de l'index pour vérification visuelle rapide
            h, w, _ = frame.shape
            px, py = int(landmarks[0].x * w), int(landmarks[0].y * h)
            cv2.circle(frame, (px, py), 8, color, -1)

        # Afficher le nombre d'enregistrements actuels à l'écran
        cv2.putText(frame, f"Geste: '{gesture_name}' | Enregistre: {saved_count}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.imshow("Collecte de Donnees", frame)

        key = cv2.waitKey(1) & 0xFF
        
        # Enregistrer la pose si on appuie sur ESPACE et qu'une main est détectée
        if key == ord(' ') and landmarks:
            # Normaliser les coordonnées (42 valeurs : 21 points * (x, y))
            features = normalize_landmarks(landmarks)
            
            # Ajouter le nom du geste à la fin (notre "label")
            row = features + [gesture_name]
            
            # Sauvegarder dans le fichier CSV
            file_exists = os.path.exists(csv_filename)
            with open(csv_filename, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
                
            saved_count += 1
            print(f"Pose #{saved_count} enregistrée.")

        # Quitter
        elif key == ord('q'):
            break

    cap.release()
    detector.close()
    cv2.destroyAllWindows()
    print(f"\nTerminé ! {saved_count} exemples enregistrés dans '{csv_filename}'.")

if __name__ == "__main__":
    main()
