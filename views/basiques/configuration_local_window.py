import json  # Module pour manipuler les fichiers JSON
import requests  # Importation de la bibliothèque requests pour faire des requêtes HTTP
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from views.basiques.administrateur_window import AdministrateurWindow  # Importer la fenêtre de création de premier compte
import os  # Module pour vérifier l'existence du fichier
from views.basiques.connexion_window import ConnexionWindow  # Importation de la fenêtre de connexion



# Nom des fichiers de configuration JSON
CONFIG_FILE = "config.json"


class ConfigurationLocalWindow(QWidget):
    def __init__(self, save_configuration_callback=None):
        super().__init__()

        self.setWindowTitle("Configuration de l'API Local")
        self.setFixedSize(350, 200)

        # Définir l'icône de la fenêtre à partir de la classe AppConfig
        self.setWindowIcon(ImagePath.get_icon())

        self.setLayout(QVBoxLayout())

        # Champ pour l'URL de l'API
        self.api_url_input = QLineEdit()
        self.api_url_input.setPlaceholderText("Entrez l'URL de l'API")
        self.layout().addWidget(QLabel("URL de l'API :"))
        self.layout().addWidget(self.api_url_input)

        # Bouton pour enregistrer la configuration
        save_button = QPushButton("Enregistrer")
        save_button.clicked.connect(self.save_config)
        save_button.setStyleSheet(
            "background-color: #F45B3C; color: #FFFFFF; font-size: 18px; padding: 5px 10px; border-radius: 8px; margin-top: 15px"
        )
        self.layout().addWidget(save_button)

    def save_configuration(self, config_data):
        """Sauvegarde les données de configuration dans le fichier JSON sans écraser les données existantes."""
        # Charger les données existantes si le fichier existe
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as file:
                    existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}  # Si le fichier est vide ou corrompu, commencer avec un dictionnaire vide
        else:
            existing_data = {}

        # Mettre à jour les données existantes avec les nouvelles configurations
        existing_data.update(config_data)

        # Enregistrer les données mises à jour dans le fichier JSON
        with open(CONFIG_FILE, "w") as file:
            json.dump(existing_data, file, indent=4)

    def save_config(self):
        """
        Enregistre l'URL et le jeton de l'API dans le fichier de configuration.
        """
        api_url = self.api_url_input.text().strip()

        if api_url:
            # Créer les nouvelles données de configuration
            config_data = {
                "api_config": {
                    "url": api_url,
                    "token": "null"
                }
            }
            self.save_configuration(config_data)  # Sauvegarder la configuration sans supprimer le contenu existant
            QMessageBox.information(self, "Succès", "Configuration enregistrée avec succès.")
            
            # Faire une requête à l'API pour voir s'il existe déjà un administrateur
            self.check_existing_administrators(api_url)
        else:
            QMessageBox.warning(self, "Erreur", "L'URL de l'API et le jeton d'authentification ne peuvent pas être vides.")

    def check_existing_administrators(self, api_url):
        """
        Vérifie si un administrateur existe déjà en faisant une requête à l'API.
        """
        
        try:
            # Faire la requête pour obtenir le nombre d'administrateurs
            response = requests.get(f"{api_url}/nombre-administrateur")  # Remplace par l'endpoint correct de l'API
            if response.status_code == 200:
                data = response.json()
                # Vérifie si des administrateurs existent
                if data['code'] == 616:
                    # Si aucun administrateur existe, ouvrir la fenêtre de connexion
                    self.open_conneion_window()
                else:
                    # Si aucun administrateur n'existe, ouvrir la fenêtre de création du premier compte
                    self.open_administrateur_window()
            else:
                # En cas d'erreur de l'API
                QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API ou d'obtenir les administrateurs.")
                
        except requests.exceptions.RequestException as e:
            # En cas d'exception lors de la requête
            QMessageBox.warning(self, "Erreur de connexion", f"Erreur de connexion à l'API : {e}")
        

    def open_administrateur_window(self):
        """
        Affiche la fenêtre pour créer le premier compte administrateur.
        """
        self.hide()  # Cacher la fenêtre actuelle
        self.administrateur_window = AdministrateurWindow()  # Passer l'instance courante en tant que parent à AdministrateurWindow
        self.administrateur_window.show()


    def open_conneion_window(self):
        """
        Affiche la fenêtre de connexion.
        """
        self.hide()  # Cacher la fenêtre actuelle
        # Affiche la fenêtre de connexion si non connecté
        self.connexion_window = ConnexionWindow()
        self.connexion_window.show()