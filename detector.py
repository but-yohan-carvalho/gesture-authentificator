import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandDetector:
    def __init__(self, model_path="hand_landmarker.task"):
        # Configurer le détecteur de mains
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1
        )
        # Créer l'instance du détecteur
        self.detector = vision.HandLandmarker.create_from_options(options)

    def detect(self, frame_rgb, timestamp_ms):
        # Convertir l'image numpy (RGB) en objet Image MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        
        # Lancer la détection
        result = self.detector.detect_for_video(mp_image, timestamp_ms)
        
        # S'il y a des détections, on retourne le premier ensemble de points (la première main)
        if result.hand_landmarks:
            return result.hand_landmarks[0]
        return None

    def close(self):
        # Libérer les ressources du détecteur
        self.detector.close()
