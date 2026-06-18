# 📋 Feuille de Route - Gesture Authentificator

Ce document sert de fil conducteur pour le développement pas à pas de votre système d'authentification par gestes. Nous le mettrons à jour au fur et à mesure de notre progression.

---

## 🗺️ Les Étapes du Projet

### 🟩 Étape 1 : Initialisation & Capture Vidéo (Terminée)
* **Objectif** : Mettre en place la capture de la webcam et détecter la main de l'utilisateur avec MediaPipe.
* **Fichiers concernés** :
  * [detector.py](file:///c:/Users/Yohan/projets_persos/gesture-authentificator/detector.py) (Classe d'analyse d'image)
  * [main.py](file:///c:/Users/Yohan/projets_persos/gesture-authentificator/main.py) (Boucle principale OpenCV et affichage)
* **🧠 Compétences acquises** :
  * Capturer et manipuler des flux vidéo en direct avec **OpenCV**.
  * Utiliser la nouvelle **API Tasks de MediaPipe** pour extraire les repères (landmarks) d'une main.
  * Adapter des coordonnées normalisées ($0.0$ à $1.0$) en coordonnées pixels sur l'image.
  * Structurer un projet Python de manière modulaire (séparation détection/affichage).

---

### 🟩 Étape 2 : Reconnaissance de Gestes par Machine Learning (Terminée)
* **Objectif** : Enregistrer un jeu de données de gestes, entraîner un modèle de classification (ex: KNN avec Scikit-Learn), et l'utiliser pour prédire les gestes en temps réel.
* **Fichiers concernés** :
  * [collect_data.py](file:///c:/Users/Yohan/projets_persos/gesture-authentificator/collect_data.py) [NEW] (Enregistrement des positions de mains pour créer notre dataset)
  * [train_model.py](file:///c:/Users/Yohan/projets_persos/gesture-authentificator/train_model.py) [NEW] (Entraînement et sauvegarde du modèle)
  * Modification de [detector.py](file:///c:/Users/Yohan/projets_persos/gesture-authentificator/detector.py) (Chargement du modèle et prédiction en temps réel)
* **🧠 Compétences acquises** :
  * Créer et formater un jeu de données (dataset) à partir de flux vidéo.
  * Utiliser **Scikit-Learn** pour entraîner un modèle de classification de données tabulaires (KNN).
  * Sauvegarder et charger un modèle d'IA en production (sérialisation avec pickle).

---

### 🟨 Étape 3 : Gestion de la Séquence (Le "Mot de passe") (En cours)
* **Objectif** : Mettre en place un système qui valide une combinaison de gestes dans un ordre précis (ex: `[POING, V, MAIN_OUVERTE]`) avec une temporisation (l'utilisateur doit maintenir le geste 1.5 seconde pour le valider).
* **🧠 Compétences à acquérir** :
  * Concevoir une **machine à états finis** (Finite State Machine) en Python.
  * Gérer les notions de temps (délais, temps d'attente, réinitialisation si le geste est faux).

---

### ⬜ Étape 4 : Déclenchement d'Actions Système
* **Objectif** : Associer la réussite du mot de passe gestuel à une action réelle sur votre ordinateur (ex: ouvrir le Bloc-notes, lancer un script, ou afficher un message de succès).
* **🧠 Compétences à acquérir** :
  * Interagir avec le système d'exploitation Windows à l'aide des modules Python `os` et `subprocess`.
  * Gérer le lancement de processus externes de manière sécurisée.

---

### ⬜ Étape 5 : Polissage & Interface Dynamique
* **Objectif** : Rendre l'application visuellement attrayante en ajoutant des retours visuels en temps réel sur la vidéo (barre de chargement de validation du geste, couleurs qui changent en fonction de l'état, texte explicatif).
* **🧠 Compétences à acquérir** :
  * Maîtriser le dessin avancé sur OpenCV (cercles, rectangles de progression, polices).
  * Améliorer l'expérience utilisateur (UX) dans une application de vision par ordinateur.

---

### ⬜ Étape 6 : Empaquetage & Création d'un Exécutable (.exe)
* **Objectif** : Transformer votre code Python en un logiciel autonome (un fichier `.exe` exécutable) utilisable en un double-clic, sans nécessiter d'installer Python ou les dépendances manuellement sur l'ordinateur cible.
* **🧠 Compétences à acquérir** :
  * Configurer et utiliser des outils de packaging Python comme **PyInstaller**.
  * Intégrer les fichiers de ressources (comme les fichiers `.pkl` du modèle de gestes) au sein du binaire final.
  * Créer un lanceur indépendant et éventuellement un installateur.

