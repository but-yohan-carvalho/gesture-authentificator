import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pickle
from sklearn.neighbors import KNeighborsClassifier
import os
import sys

def resource_path(relative_path):
    """Obtient le chemin absolu vers la ressource, compatible avec PyInstaller."""
    try:
        # PyInstaller extrait les ressources dans un dossier temporaire _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HandDetector:
    def __init__(self, model_path="hand_landmarker.task", pickle_filename="gesture_model.pkl"):
        # Résoudre les chemins compatibles avec la compilation
        resolved_model_path = resource_path(model_path)
        resolved_pickle_path = resource_path(pickle_filename)

        # Configurer le détecteur de mains
        base_options = python.BaseOptions(model_asset_path=resolved_model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        # Créer l'instance du détecteur
        self.detector = vision.HandLandmarker.create_from_options(options)

        with open(resolved_pickle_path, 'rb') as f:
            self.model = pickle.load(f)

    def detect(self, frame_rgb, timestamp_ms):
        # Convertir l'image numpy (RGB) en objet Image MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        # Lancer la détection
        result = self.detector.detect_for_video(mp_image, timestamp_ms)
        
        # S'il y a des détections, on retourne le premier ensemble de points (la première main)
        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None

    def _normalize_landmarks(self, landmarks):
        # Prendre le poignet (point 0) comme point de référence (origine)
        base_x = landmarks[0].x
        base_y = landmarks[0].y
        
        # Rendre les coordonnées relatives au poignet
        relative_coords = []
        for lm in landmarks:
            relative_coords.append(lm.x - base_x)
            relative_coords.append(lm.y - base_y)
            
        # Mettre à l'échelle pour que les valeurs soient comprises entre -1.0 et 1.0
        max_val = max(abs(val) for val in relative_coords)
        if max_val > 0:
            relative_coords = [val / max_val for val in relative_coords]
            
        return relative_coords

    def predict_gesture(self, landmarks):
        if not landmarks:
            return None
            
        # Normaliser les repères de la main
        features = self._normalize_landmarks(landmarks)
        
        # Prédire le geste (on passe un tableau 2D [features])
        prediction = self.model.predict([features])
        return prediction[0]


    def close(self):
        # Libérer les ressources du détecteur
        self.detector.close()
