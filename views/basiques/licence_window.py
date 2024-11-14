# views/licence_window.py

import json  # Importation de la bibliothèque JSON
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from services.api_client import APIClient  # Importation du client API pour les requêtes HTTP
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from views.basiques.bienvenue_window import WelcomeWindow  # Importation de la fenêtre de bienvenue
import os  # Pour vérifier l'existence des fichiers et gérer les chemins


class LicenceWindow(QWidget):
    def __init__(self):
        """
        Initialise la fenêtre de vérification de licence.
        go_to_bienvenue_callback : une fonction de rappel qui est appelée après une vérification réussie de la licence.
        """
        super().__init__()

        # Définir le titre de la fenêtre
        self.setWindowTitle("Vérification de Licence")
        # Définir la taille fixe de la fenêtre
        self.setFixedSize(500, 300)

        self.setWindowIcon(ImagePath.get_icon())

        # Créer un layout vertical pour l'agencement des widgets
        layout = QVBoxLayout()

        # Ajouter le logo de l'application
        self.logo_label = QLabel(self)
        pixmap = QPixmap("assets/images/logoMemgesth.png")
        self.logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Ajouter un label et un champ de saisie pour la clé d'authentification
        self.institut_label = QLabel("Entrez votre clé d'authentification :")
        self.institut_input = QLineEdit()
        layout.addWidget(self.institut_label)
        layout.addWidget(self.institut_input)

        # Ajouter un label et un champ de saisie pour la clé de licence
        self.licence_label = QLabel("Entrez votre clé de licence :")
        self.licence_input = QLineEdit()
        layout.addWidget(self.licence_label)
        layout.addWidget(self.licence_input)

        self.submit_button = QPushButton("Vérifier Licence")
        self.submit_button.setStyleSheet(
            "background-color: #121F91; color: #FFFFFF; font-size: 18px; padding: 5px 10px; border-radius: 8px; margin-top: 15px"
        )
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # Connecter le clic du bouton à la méthode de vérification de la clé
        self.submit_button.clicked.connect(self.verify_licence)

    def verify_licence(self):
        """
        Vérifie la clé de licence via une requête API.
        Si la clé est valide, la fenêtre de bienvenue s'affiche et enregistre la clé dans config.json.
        """
        authentification_key = self.institut_input.text()  # Récupère la clé d'authentification entrée par l'utilisateur
        licence_key = self.licence_input.text()  # Récupère la clé de licence entrée par l'utilisateur
        api_url = "http://clesaas.amosag.local/api"  # URL de l'API

        client = APIClient(api_url, authentification_key, licence_key)
        resultat = False  # Initialisation de la variable pour éviter l'erreur

        try:
            
            # Effectuer une requête GET pour vérifier la clé de licence
            response = client.get(f"{authentification_key}?cle_licence={licence_key}")
            
            if response['code'] == 200:
                resultat = True  # Marquer comme succès
            else:
                QMessageBox.warning(self, "Echec", response['message'])  # Affiche un message d'erreur

                
        except Exception as e:
            # Affiche une erreur en cas de problème de connexion
            QMessageBox.critical(self, "Erreur", f"Erreur de connexion : {str(e)}")
            
        # Si la vérification a réussi, exécuter le reste du code
        if resultat:
            # Enregistrer la clé dans config.json
            self.save_data_key(authentification_key, licence_key)

            # Transition vers la fenêtre de bienvenue
            self.go_to_bienvenue_window()

            # Affiche un message de succès
            QMessageBox.information(self, "Succès", "Licence vérifiée avec succès.")
        

    def save_data_key(self, authentification_key, licence_key):
        """
        Enregistre la clé de licence dans un fichier config.json.
        """
        config_file = "config.json"
        config_data = {}

        if os.path.exists(config_file):
            with open(config_file, 'r') as file:
                config_data = json.load(file)

        config_data["authentificationKey"] = licence_key
        config_data["licenceKey"] = authentification_key

        with open(config_file, 'w') as file:
            json.dump(config_data, file, indent=4)
            
    def go_to_bienvenue_window(self):
        """
        Affiche la fenêtre de bienvenue.
        """
        # Regarder voir si dans le fichier config.json y'a déjà 
        self.hide()  # Cacher la fenêtre actuelle
        self.bienvenue_window = WelcomeWindow()  # Passer l'instance courante en tant que parent à ConfigWindow
        self.bienvenue_window.show()

