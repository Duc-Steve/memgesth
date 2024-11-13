from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from services.api_client import APIClient
from views.basiques.connexion_window import ConnexionWindow  # Importer ConnexionWindow pour la redirection
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
import json
from services.configuration_manager import get_authentication_key, get_license_key, get_api_url, get_api_token
import requests  # Importation de la bibliothèque requests pour faire des requêtes HTTP




# Nom des fichiers de configuration JSON
CONFIG_FILE = "config.json"

class AdministrateurWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Création du Premier Compte Administrateur")
        self.setFixedSize(450, 350)

        self.setWindowIcon(ImagePath.get_icon())
        
        self.setLayout(QVBoxLayout())

        # Champs pour le nom, prénom, email et mot de passe
        self.nom_input = QLineEdit()
        self.nom_input.setPlaceholderText("Entrez votre nom")
        self.layout().addWidget(QLabel("Nom :"))
        self.layout().addWidget(self.nom_input)

        self.prenom_input = QLineEdit()
        self.prenom_input.setPlaceholderText("Entrez votre prénom")
        self.layout().addWidget(QLabel("Prénom :"))
        self.layout().addWidget(self.prenom_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Entrez votre email")
        self.layout().addWidget(QLabel("Email :"))
        self.layout().addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.layout().addWidget(QLabel("Mot de passe :"))
        self.layout().addWidget(self.password_input)
        
        # Ajouter les boutons création du compte et connexion
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 30, 0, 0)  # Marges pour le bouton
        create_account_button = QPushButton("Créer le compte")
        create_account_button.clicked.connect(self.create_account)

        # Styles pour les boutons
        create_account_button.setStyleSheet("background-color: #F45B3C; font-size: 16px; color: white; border-radius: 5px; padding: 5px 15px 5px 15px;")
        
        # Alignement à droite des boutons
        button_layout.addStretch()  # Ajoute un espace élastique pour pousser les boutons à droite
        button_layout.addWidget(create_account_button)
        
        self.layout().addLayout(button_layout)


    def create_account(self):
        """
        Envoie une requête pour créer le premier compte administrateur.
        """
        # Récupérer les valeurs des champs
        nom = self.nom_input.text().strip()
        prenom = self.prenom_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not all([nom, prenom, email, password]):
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
            return

        # Préparer les données à envoyer à l'API
        account_data = {
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "password": password
        }

        # Ajouter le suffixe /create-first-admin à l'URL de l'API
        response = requests.post(f"{get_api_url()}/create-first-admin", account_data)  # Remplace par l'endpoint correct de l'API
        
        if response.status_code == 200:
            data = response.json()
            # Si le code est succes
            if data['code'] == 200:
                QMessageBox.information(self, "Redirection", "Votre compte a été créé. Vous pouvez maintenant vous connecter.")
                
                with open(CONFIG_FILE, 'r+') as config_file:
                    config_data = json.load(config_file)
                    config_data["administrateurFirst"] = "oui"  # Ajoute ou met à jour la clé
                    config_file.seek(0)
                    json.dump(config_data, config_file, indent=4)
                    config_file.truncate()
                
                self.connexion_window()
            else:
                # Afficher une boîte de message avec un titre correct
                QMessageBox.warning(self, "Erreur", data['message'])
        else:
            # En cas d'erreur de l'API
            QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API ou d'obtenir les administrateurs.")


    def connexion_window(self):
        """
        Affiche la fenêtre ConnexionWindow
        """
        self.hide()  # Cacher la fenêtre actuelle
        self.connexion_window_best = ConnexionWindow()  # Passer l'instance courante en tant que parent à connexion_window
        self.connexion_window_best.show()