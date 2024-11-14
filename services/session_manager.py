import json
import os

class SessionManager:
    """Gestionnaire de session utilisateur pour stocker et gérer l'état de connexion de l'utilisateur."""

    def __init__(self):
        # Nom du fichier où les informations de session seront stockées localement
        self.session_file = "admin_session.json"

    def save_session(self, user_data):
        """
        Enregistre les informations de l'utilisateur dans un fichier JSON.

        Args:
            user_data (dict): Dictionnaire contenant les informations de l'utilisateur 
                              à enregistrer dans la session, comme l'ID utilisateur, 
                              le nom d'utilisateur, le token d'authentification, etc.
        """
        # Ouvre le fichier en mode écriture et enregistre les données de session sous format JSON
        with open(self.session_file, 'w') as file:
            json.dump(user_data, file)

    def load_session(self):
        """
        Charge les informations de session utilisateur si elles existent.

        Returns:
            dict: Les informations de session utilisateur chargées depuis le fichier JSON, 
                  ou None si le fichier de session n'existe pas.
        """
        # Vérifie si le fichier de session existe
        if os.path.exists(self.session_file):
            # Si le fichier existe, il est ouvert et les données JSON sont chargées et renvoyées
            with open(self.session_file, 'r') as file:
                return json.load(file)
        # Retourne None si le fichier n'existe pas
        return None

    def clear_session(self):
        """
        Supprime les informations de session utilisateur.

        Efface le fichier de session s'il existe, pour déconnecter l'utilisateur.
        """
        # Vérifie si le fichier de session existe
        if os.path.exists(self.session_file):
            # Supprime le fichier de session pour effacer les données utilisateur
            os.remove(self.session_file)

    def is_logged_in(self):
        """
        Vérifie si l'utilisateur est connecté.

        Returns:
            bool: True si l'utilisateur a une session valide, False sinon.
        """
        # Charge la session et vérifie si des informations de session sont présentes
        return self.load_session() is not None

    def logout(self):
        """
        Déconnecte l'utilisateur en effaçant les informations de session.
        """
        self.clear_session()  # Appelle la méthode pour effacer la session
        print("Utilisateur déconnecté avec succès.")  # Message de confirmation (peut être modifié selon les besoins)