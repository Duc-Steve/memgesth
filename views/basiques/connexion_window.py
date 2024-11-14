from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QLineEdit, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from services.api_client import APIClient  # Requêtes API
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from services.session_manager import SessionManager  # Importer le gestionnaire de session
from services.configuration_manager import get_authentication_key, get_license_key, get_api_url, get_api_token
import requests  # Importation de la bibliothèque requests pour faire des requêtes HTTP
import json  # Module pour manipuler les fichiers JSON


# Nom des fichiers de configuration JSON
ADMIN_SESSION_FILE = "admin_session.json"


class ConnexionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(400, 300)
        self.setWindowIcon(ImagePath.get_icon())

        # Initialisation du gestionnaire de session
        self.session_manager = SessionManager()
        
        # Layout et champs de texte
        layout = QVBoxLayout()
        
        # Ajouter le logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("assets/logoMemgesth.png")
        self.logo_label.setPixmap(pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Adresse mail")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Se connecter")
        self.login_button.setStyleSheet(
            "background-color: #121F91; color: #FFFFFF; font-size: 18px; padding: 5px 10px; border-radius: 8px; margin-top: 15px"
        )

        # Connexion du bouton de connexion
        self.login_button.clicked.connect(self.authenticate_admin)

        # Ajout des widgets
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # Configuration du conteneur central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def authenticate_admin(self):
        """Vérifie les informations de connexion de l'utilisateur."""
        email = self.email_input.text()
        password = self.password_input.text()

        # Préparer les données à envoyer à l'API
        account_data = {
            "email": email,
            "password": password
        }
    
        # Ajouter le suffixe /authentification à l'URL de l'API
        response = requests.post(f"{get_api_url()}/authentification", account_data)  # Remplace par l'endpoint correct de l'API
            
        if response.status_code == 200:
            data = response.json()
            # Si le code est succes
            if data['code'] == 200:
                
                # Récupérer le token et les détails de l'utilisateur
                token = data['token']
                admin_data = data['admin']  # Assurez-vous que la réponse JSON contient une clé 'admin'

                if token and admin_data:
                    # Enregistrer l'administrateur et son token dans le fichier de session JSON
                    session_data = {
                        "token": token,
                        "admin": admin_data
                    }
                    with open(ADMIN_SESSION_FILE, 'w') as session_file:
                        json.dump(session_data, session_file)

                    # Ouvrir la fenêtre globale après connexion réussie
                    self.open_global_action()
                else:
                    QMessageBox.warning(self, "Erreur", "Données de session manquantes dans la réponse.")
                    
                
                
            else:
                # Afficher une boîte de message avec un titre correct
                QMessageBox.warning(self, "Erreur", data['message'])
        else:
            # En cas d'erreur de l'API
            QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API.")
         
    def open_global_action(self):
        from views.fenetres.global_action_window import GlobaleActionWindow  # Importation de la fenêtre GlobaleAction
        """Ouvre le tableau de bord après connexion."""
        self.hide()  # Cacher la fenêtre actuelle
        self.global_action_window = GlobaleActionWindow()  # Remplacez par votre fenêtre principale
        self.global_action_window.show()
