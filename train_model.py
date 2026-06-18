import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report

# Chemin du dataset et du modèle à sauvegarder
CSV_FILENAME = "gestures_dataset.csv"
MODEL_FILENAME = "gesture_model.pkl"

def main():
    # --- ÉTAPE 1 : Chargement des données ---
    print("Chargement des données...")
    df = pd.read_csv(CSV_FILENAME, header=None)

    # --- ÉTAPE 2 : Séparation des caractéristiques (X) et des étiquettes (y)    
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    
    # --- ÉTAPE 3 : Division en jeu d'entraînement et de test ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    
    
    # --- ÉTAPE 4 : Initialisation et entraînement du modèle ---
    print("Entraînement du modèle...")  
    model = KNeighborsClassifier(n_neighbors=5)
    model.fit(X_train, y_train)
    
    # --- ÉTAPE 5 : Évaluation du modèle ---
    print("Évaluation du modèle...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Précision: {acc*100:.2f}%")
    print("\nRapport de classification :")
    print(classification_report(y_test, y_pred))

    
    # --- ÉTAPE 6 : Sauvegarde du modèle ---
    print(f"Sauvegarde du modèle dans {MODEL_FILENAME}...")

    with open(MODEL_FILENAME, 'wb') as f:
        pickle.dump(model, f)
    
    print("Entraînement terminé avec succès !")

if __name__ == "__main__":
    main()
