import time

class GestureSequenceManager:
    def __init__(self, target_sequence, hold_duration=1.5, error_timeout=0.8, inactivity_timeout=3.0):
        """
        Gère la validation d'une séquence de gestes (mot de passe).
        
        :param target_sequence: Liste de chaînes de caractères représentant l'ordre des gestes.
        :param hold_duration: Temps requis (en secondes) pour maintenir un geste correct.
        :param error_timeout: Temps de grâce (en secondes) pendant lequel un mauvais geste est toléré
                              avant de réinitialiser la séquence.
        :param inactivity_timeout: Temps maximal (en secondes) d'absence de geste avant réinitialisation.
        """
        self.target_sequence = [g.lower() for g in target_sequence]
        self.hold_duration = hold_duration
        self.error_timeout = error_timeout
        self.inactivity_timeout = inactivity_timeout
        
        self.current_step = 0
        self.is_authenticated = False
        
        self.last_gesture = None
        self.gesture_start_time = None
        self.error_start_time = None
        self.last_activity_time = time.time()
        self.authenticated_time = None
        
        self.wrong_gesture_active = False

    def reset(self):
        """Réinitialise complètement l'état de la machine à états."""
        self.current_step = 0
        self.is_authenticated = False
        self.last_gesture = None
        self.gesture_start_time = None
        self.error_start_time = None
        self.last_activity_time = time.time()
        self.authenticated_time = None
        self.wrong_gesture_active = False

    def update(self, gesture):
        """
        Met à jour l'état du gestionnaire avec le geste actuel.
        
        :param gesture: Nom du geste détecté (str) ou None si aucun geste/main.
        """
        now = time.time()
        
        # 1. Si déjà authentifié, on reste dans cet état pendant 5 secondes puis on reverrouille
        if self.is_authenticated:
            if now - self.authenticated_time > 5.0:
                self.reset()
            return
            
        # 2. Gestion de l'inactivité (si aucun geste/main n'est détecté)
        if gesture is None:
            # Si on a déjà commencé la séquence, on vérifie le timeout d'inactivité
            if self.current_step > 0 and (now - self.last_activity_time > self.inactivity_timeout):
                print("[SequenceManager] Réinitialisation : Inactivité prolongée.")
                self.reset()
                return
            
            # Si pas de geste, on met en pause les compteurs temporels de maintien/erreur
            self.gesture_start_time = None
            self.error_start_time = None
            self.last_gesture = None
            self.wrong_gesture_active = False
            return

        # Un geste est détecté, on met à jour le temps de dernière activité
        self.last_activity_time = now
        gesture = gesture.lower()
        expected_gesture = self.target_sequence[self.current_step]

        # 3. Le geste correspond à celui attendu à cette étape
        if gesture == expected_gesture:
            # Réinitialiser le compteur d'erreurs
            self.error_start_time = None
            self.wrong_gesture_active = False
            
            # Si on commence tout juste à faire ce geste
            if self.last_gesture != expected_gesture or self.gesture_start_time is None:
                self.gesture_start_time = now
                print(f"[SequenceManager] Début du maintien du geste correct : '{gesture}'")
            else:
                # Si le geste est maintenu depuis assez longtemps
                if now - self.gesture_start_time >= self.hold_duration:
                    self.current_step += 1
                    self.gesture_start_time = None
                    self.last_gesture = None
                    print(f"[SequenceManager] Geste '{gesture}' validé ! Étape suivante : {self.current_step}/{len(self.target_sequence)}")
                    
                    # Vérifier si toute la séquence est validée
                    if self.current_step == len(self.target_sequence):
                        self.is_authenticated = True
                        self.authenticated_time = now
                        print("[SequenceManager] ACCÈS AUTORISÉ ! Séquence correcte complétée.")
                        return
                        
        # 4. Le geste ne correspond pas à celui attendu
        else:
            # On réinitialise le compteur de maintien du geste correct
            self.gesture_start_time = None
            
            # Si on a déjà commencé à valider la séquence (étape > 0)
            if self.current_step > 0:
                # Si on commence tout juste à faire un mauvais geste
                if not self.wrong_gesture_active or self.last_gesture != gesture:
                    self.error_start_time = now
                    self.wrong_gesture_active = True
                    print(f"[SequenceManager] Geste incorrect détecté : '{gesture}' au lieu de '{expected_gesture}'. Début du temps de grâce.")
                else:
                    # Si le mauvais geste est maintenu au-delà du temps de grâce
                    if now - self.error_start_time >= self.error_timeout:
                        print(f"[SequenceManager] Réinitialisation : Mauvais geste '{gesture}' maintenu trop longtemps.")
                        self.reset()
                        return

        self.last_gesture = gesture

    def get_progress(self):
        """
        Retourne la progression du maintien du geste actuel (entre 0.0 et 1.0).
        """
        if self.gesture_start_time is None:
            return 0.0
        elapsed = time.time() - self.gesture_start_time
        return min(1.0, max(0.0, elapsed / self.hold_duration))

    def get_state_string(self):
        """Retourne l'état actuel sous forme de texte pour l'affichage."""
        if self.is_authenticated:
            return "ACCES AUTORISE"
        elif self.current_step > 0:
            return f"VALIDATION: {self.current_step}/{len(self.target_sequence)}"
        else:
            return "VERROUILLE"


# --- Zone de Test Unitaire de la logique ---
if __name__ == "__main__":
    print("=== Démarrage des tests unitaires de la logique ===")
    seq = ["poing", "v", "poing"]
    manager = GestureSequenceManager(seq, hold_duration=1.0, error_timeout=0.5, inactivity_timeout=1.5)
    
    print("\n1. Test de validation complète de la séquence")
    manager.reset()
    # Simuler "poing" pendant 1.1s
    manager.update("poing")
    time.sleep(0.5)
    manager.update("poing")
    time.sleep(0.6)
    manager.update("poing") # Devrait valider étape 1
    
    # Transition vers "v" (avec une petite pause sans geste)
    manager.update(None)
    time.sleep(0.2)
    
    # Simuler "v" pendant 1.1s
    manager.update("v")
    time.sleep(0.5)
    manager.update("v")
    time.sleep(0.6)
    manager.update("v") # Devrait valider étape 2
    
    # Simuler "poing" pendant 1.1s
    manager.update("poing")
    time.sleep(1.1)
    manager.update("poing") # Devrait authentifier !
    
    print(f"État final : {manager.get_state_string()} | Authentifié : {manager.is_authenticated}")
    
    print("\n2. Test de réinitialisation par mauvais geste")
    manager.reset()
    # Valider premier geste
    manager.update("poing")
    time.sleep(1.1)
    manager.update("poing")
    print(f"Étape courante : {manager.current_step} (Attendu: 1)")
    
    # Envoyer un mauvais geste
    manager.update("trois")
    time.sleep(0.2)
    manager.update("trois") # Dans le temps de grâce
    print(f"Après 0.2s de mauvais geste, étape = {manager.current_step} (Attendu: 1)")
    
    time.sleep(0.4)
    manager.update("trois") # Dépasse 0.5s d'erreur -> Reset !
    print(f"Après 0.6s de mauvais geste, étape = {manager.current_step} (Attendu: 0)")

    print("\n3. Test de réinitialisation par inactivité")
    manager.reset()
    # Valider premier geste
    manager.update("poing")
    time.sleep(1.1)
    manager.update("poing")
    print(f"Étape courante : {manager.current_step} (Attendu: 1)")
    
    # Plus de geste
    manager.update(None)
    time.sleep(1.6) # Dépasse inactivity_timeout de 1.5s
    manager.update(None)
    print(f"Après 1.6s d'inactivité, étape = {manager.current_step} (Attendu: 0)")
    print("=== Fin des tests unitaires ===")
