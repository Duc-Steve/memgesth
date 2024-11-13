import requests

class APIClient:
    def __init__(self, api_url, api_key, licence_key):
        """
        Initialise l'instance du client API avec l'URL de base et la clé API.
        
        :param api_url: URL de base de l'API (ex: "https://api.exemple.com")
        :param api_key: Clé d'authentification pour l'API (ex: "votre_clé_secrète")
        :param licence_key: Clé de licence pour l'API (ex: "votre_clé_secrète")
        """
        self.api_url = api_url  # Stocke l'URL de base de l'API
        self.api_key = api_key  # Stocke la clé d'authentification
        self.licence_key = licence_key # Stocke la clé de licence

    def get(self, endpoint):
        """
        Effectue une requête GET à l'API avec l'URL de l'endpoint fourni.
        
        :param endpoint: Chemin de l'endpoint (ex: "utilisateurs" pour "/utilisateurs")
        :return: Réponse de l'API sous forme de dictionnaire (ou lève une exception en cas d'erreur)
        """
        # Prépare les en-têtes de requête avec la clé API pour l'authentification
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Effectue la requête GET à l'endpoint complet en ajoutant l'URL de base
        response = requests.get(f"{self.api_url}/{endpoint}", headers=headers)
        
        # Vérifie si la requête a échoué et lève une exception si c'est le cas
        response.raise_for_status()
        
        # Retourne la réponse JSON sous forme de dictionnaire Python
        return response.json()

    def post(self, endpoint, data):
        """
        Effectue une requête POST à l'API avec l'URL de l'endpoint et les données fournies.
        
        :param endpoint: Chemin de l'endpoint (ex: "utilisateurs" pour "/utilisateurs")
        :param data: Données à envoyer dans la requête POST sous forme de dictionnaire (ex: {"nom": "Jean"})
        :return: Réponse de l'API sous forme de dictionnaire (ou lève une exception en cas d'erreur)
        """
        # Prépare les en-têtes de requête avec la clé API pour l'authentification
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Effectue la requête POST à l'endpoint complet avec les données JSON et les en-têtes
        response = requests.post(f"{self.api_url}/{endpoint}", json=data, headers=headers)
        
        # Vérifie si la requête a échoué et lève une exception si c'est le cas
        response.raise_for_status()
        
        # Retourne la réponse JSON sous forme de dictionnaire Python
        return response.json()
