import cv2
import time
from detector import HandDetector
from sequence_manager import GestureSequenceManager

# Liste des connexions pour dessiner le squelette de la main
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
]

def draw_hand(frame, landmarks):
    h, w, _ = frame.shape
    pixel_landmarks = []
    
    # 1. Dessiner les points des articulations
    for lm in landmarks:
        px, py = int(lm.x * w), int(lm.y * h)
        pixel_landmarks.append((px, py))
        cv2.circle(frame, (px, py), 5, (0, 255, 0), -1)

    # 2. Dessiner les lignes reliant les articulations
    for connection in HAND_CONNECTIONS:
        start_idx, end_idx = connection
        cv2.line(frame, pixel_landmarks[start_idx], pixel_landmarks[end_idx], (255, 0, 0), 2)

def main():
    # Initialiser la caméra et notre détecteur de mains
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    
    # Définir le mot de passe (séquence de gestes attendue)
    # MODIFIEZ CETTE LISTE selon les gestes que vous avez enregistrés
    target_sequence = ["poing", "v", "main_ouverte"]
    auth_manager = GestureSequenceManager(target_sequence, hold_duration=1.5, error_timeout=0.8, inactivity_timeout=3.0)
    
    start_time = time.time()
    print("Démarrage. Appuyez sur 'q' pour quitter.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Effet miroir pour l'affichage
        frame = cv2.flip(frame, 1)

        # MediaPipe a besoin de RGB, OpenCV utilise du BGR
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        timestamp_ms = int((time.time() - start_time) * 1000)

        # Détecter la main
        landmarks = detector.detect(rgb_frame, timestamp_ms)
        gesture = None

        # Si une main est détectée, on la dessine et on prédit le geste
        if landmarks:
            draw_hand(frame, landmarks)
            gesture = detector.predict_gesture(landmarks)
            
            # Afficher le geste prédit à l'écran
            if gesture:
                cv2.putText(frame, f"Geste: {gesture.upper()}", (10, 40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

        # Mettre à jour le gestionnaire de séquence avec le geste détecté
        auth_manager.update(gesture)

        # Afficher l'état d'authentification à l'écran
        state = auth_manager.get_state_string()
        if auth_manager.is_authenticated:
            # Texte grand en vert pour signifier le succès
            cv2.putText(frame, "ACCES AUTORISE", (10, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 3, cv2.LINE_AA)
        else:
            # Texte orange/jaune pour l'état verrouillé / progression
            cv2.putText(frame, f"Etat: {state}", (10, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2, cv2.LINE_AA)
            
            # Afficher la jauge de progression sous forme de pourcentage si on maintient le bon geste
            if auth_manager.gesture_start_time is not None:
                progress = auth_manager.get_progress()
                cv2.putText(frame, f"Maintien: {int(progress * 100)}%", (10, 110), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow("Gesture Authenticator", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fermeture propre
    cap.release()
    detector.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
