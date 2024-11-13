import json  # Module pour manipuler les fichiers JSON
import os  # Module pour vérifier l'existence de fichiers
import requests  # Module pour effectuer des requêtes HTTP
from services.api_client import APIClient  # Importation du client API pour les requêtes HTTP
from PySide6.QtWidgets import QApplication, QMessageBox  # Classes de base pour créer une application Qt
from views.basiques.connexion_window import ConnexionWindow  # Importation de la fenêtre de connexion
from views.basiques.configuration_ligne_window import ConfigurationLigneWindow  # Importation de la fenêtre de configuration ligne
from views.basiques.licence_window import LicenceWindow  # Importation de la fenêtre de gestion de licence
from views.basiques.administrateur_window import AdministrateurWindow  # Importer la fenêtre de création de premier compte
from views.basiques.choix_db_window import ChoixDbWindow  # Importer la fenêtre de choix DB
from views.basiques.configuration_local_window import ConfigurationLocalWindow  # Importation de la fenêtre de configuration local
from views.fenetres.global_action_window import GlobaleActionWindow  # Importer la fenêtre global Action



# Nom des fichiers de configuration JSON
CONFIG_FILE = "config.json"
ADMIN_SESSION_FILE = "admin_session.json"

def create_default_config():
    """ Crée un fichier de configuration par défaut s'il n'existe pas. """
    default_config = {}
    save_configuration(default_config)
    return default_config

def load_configuration():
    """ Charge les données de configuration depuis le fichier JSON. """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)  # Charge les données JSON depuis le fichier
    return create_default_config()  # Crée un fichier de configuration par défaut

def save_configuration(config_data):
    """ Sauvegarde les données de configuration dans le fichier JSON. """
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file)  # Écrit les données dans le fichier JSON

def load_user_session():
    """ Charge les données de session utilisateur depuis le fichier user_session.json. """
    if os.path.exists(ADMIN_SESSION_FILE):
        with open(ADMIN_SESSION_FILE, "r") as file:
            return json.load(file)  # Charge les données de session utilisateur
    return None  # Aucune session utilisateur trouvée

def verify_all_key(authentification_key, licence_key):
    """ Vérifie la validité des clés. """
    # api_url = "http://clesaas.amosag.local/api"
    # client = APIClient(api_url, authentification_key, licence_key)
    # try:
        # Effectuer une requête GET pour vérifier la clé de licence
        # response = client.get(f"{authentification_key}?cle_licence={licence_key}")
        
        # if response['code'] == "200":
    return True # response.json().get("status") == "ok"  # Retourne True si la clé est valide
        # else:
            # return False  # Retourne False en cas d'erreur de connexion ou de requête
    # except requests.RequestException:
        # return False  # Retourne False en cas d'erreur de connexion ou de requête

def main():
    """ Point d'entrée principal de l'application. """
    app = QApplication([])  # Crée une application Qt vide

    # Charge la configuration depuis le fichier JSON
    config = load_configuration()

   
    if "licenceKey" in config and "authentificationKey" in config:
        
        # Récupère les clés de licence et d'authentification
        licence_key = config["licenceKey"]
        authentification_key = config["authentificationKey"]
        
        # Vérifie la validité des clés
        if verify_all_key(authentification_key, licence_key):
            
            # Vérifie si le choix de la base de données a été effectué
            if "choix_localisation_db" in config:
                
                # Vérifie le choix de la base de données (en ligne ou locale)
                if config["choix_localisation_db"] == "ligne":
                    
                    # Si une clé d'identification existe
                    if "identificationKey" and "api_config" in config:
                        
                        # Vérifie l'existence d'un compte administrateur
                        if "administrateurFirst" in config:
                            
                            # Charge la session utilisateur
                            user_session = load_user_session()
                            
                            # Vérifie si l'utilisateur est connecté
                            if user_session:
                                # Affiche la fenêtre principale des actions
                                globale_action_window = GlobaleActionWindow()
                                globale_action_window.show()
                            else:
                                # Affiche la fenêtre de connexion si non connecté
                                connexion_window = ConnexionWindow()
                                connexion_window.show()
                        else:
                            # Affiche la fenêtre pour créer le premier compte administrateur
                            premier_compte_window = AdministrateurWindow()  
                            premier_compte_window.show()
                    else:
                        # Affiche la fenêtre de configuration en ligne si clé d'identification absente
                        configuration_ligne_window = ConfigurationLigneWindow() 
                        configuration_ligne_window.show()

                elif config["choix_localisation_db"] == "local":
                    
                    # Si la base de données choisie est locale
                    if "api_config" in config:
                        
                        # Vérifie l'existence d'un compte administrateur
                        if "administrateurFirst" in config:
                            
                            # Charge la session utilisateur
                            user_session = load_user_session()
                            
                            # Vérifie si l'utilisateur est connecté
                            if user_session:
                                # Affiche la fenêtre principale des actions
                                globale_action_window = GlobaleActionWindow()
                                globale_action_window.show()
                            else:
                                # Affiche la fenêtre de connexion si non connecté
                                connexion_window = ConnexionWindow()
                                connexion_window.show()
                        else:
                            premier_compte_window = AdministrateurWindow()
                            premier_compte_window.show()
                    else:
                        # Affiche la fenêtre de configuration locale si la configuration API est absente
                        configuration_local_window = ConfigurationLocalWindow()
                        configuration_local_window.show()
                else:
                    # Gère les erreurs de configuration de la base de données non reconnue
                    QMessageBox.warning(None, "Erreur", "Configuration de base de données non reconnue.")
            else:
                # Affiche la fenêtre de choix de la base de données si non définie
                choix_localisation_db_window = ChoixDbWindow()
                choix_localisation_db_window.show()
        else:
            # Affiche la fenêtre de gestion de licence en cas de clé invalide
            licence_window = LicenceWindow()
            licence_window.show()
            QMessageBox.warning(licence_window, "Licence", "Clé de licence invalide.")
    else:
        # Affiche la fenêtre de licence si aucune clé n'est trouvée
        licence_window = LicenceWindow()
        licence_window.show()

    # Exécute la boucle principale de l'application
    app.exec()

    # Exécute la boucle principale de l'application
    app.exec()

if __name__ == "__main__":
    main()  # Point d'entrée de l'application
