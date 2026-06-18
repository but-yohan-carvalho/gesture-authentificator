import cv2
import time
from detector import HandDetector

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

        # Si une main est détectée, on la dessine et on prédit le geste
        if landmarks:
            draw_hand(frame, landmarks)
            gesture = detector.predict_gesture(landmarks)
            
            # Afficher le geste prédit à l'écran
            if gesture:
                cv2.putText(frame, f"Geste: {gesture.upper()}", (10, 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


        cv2.imshow("Gesture Authenticator", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Fermeture propre
    cap.release()
    detector.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
