import json
import os

# Chemin du fichier de configuration
CONFIG_FILE_PATH = "config.json"

def load_config():
    """Charge le fichier de configuration JSON et retourne le dictionnaire des données."""
    if os.path.exists(CONFIG_FILE_PATH):
        try:
            with open(CONFIG_FILE_PATH, "r") as file:
                config_data = json.load(file)
            return config_data
        except json.JSONDecodeError:
            raise ValueError("Le fichier de configuration est corrompu.")
    else:
        raise FileNotFoundError("Le fichier de configuration n'existe pas.")

def get_authentication_key():
    """Retourne la clé d'authentification."""
    config = load_config()
    return config.get("authentificationKey")

def get_license_key():
    """Retourne la clé de licence."""
    config = load_config()
    return config.get("licenceKey")

def get_database_location_choice():
    """Retourne le choix de localisation de la base de données."""
    config = load_config()
    return config.get("choix_localisation_db")

def get_api_url():
    """Retourne l'URL de l'API."""
    config = load_config()
    api_config = config.get("api_config", {})
    return api_config.get("url")

def get_api_token():
    """Retourne le jeton de l'API."""
    config = load_config()
    api_config = config.get("api_config", {})
    return api_config.get("token")

def get_identification_key():
    """Retourne la clé d'identification."""
    config = load_config()
    return config.get("identificationKey")
