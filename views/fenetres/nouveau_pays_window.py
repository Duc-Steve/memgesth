from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from services.session_manager import SessionManager
import requests  # Importation de la bibliothèque requests pour faire des requêtes HTTP
from services.configuration_manager import get_api_url
from PySide6.QtCore import Signal




class NouveauPaysWindow(QDialog):
    # Définir un signal personnalisé
    pays_enregistre = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)

        # Configurer la fenêtre de dialogue
        self.setWindowTitle("Enregistrement d'un nouveau pays")
        self.setFixedSize(350, 200)  # Définir la taille de la fenêtre

        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())
        
        # Layout principal
        layout = QVBoxLayout()

        # Création des champs de saisie (nom, prénom, etc.)
        self.nom_label = QLabel("Nom du pays :")
        self.nom_pays = QLineEdit()
        layout.addWidget(self.nom_label)
        layout.addWidget(self.nom_pays)

        self.code_label = QLabel("Code du pays :")
        self.code_pays = QLineEdit()
        layout.addWidget(self.code_label)
        layout.addWidget(self.code_pays)

        # Ajouter les boutons Enregistrer et Annuler
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 30, 0, 0)  # Marges pour le bouton

        cancel_button = QPushButton("Annuler")
        save_button = QPushButton("Enregistrer")
        
        # Connecter les boutons à leurs actions respectives
        cancel_button.clicked.connect(self.close)  # Fermer la fenêtre à la demande
        save_button.clicked.connect(self.enregistrer_pays)  # Enregistrer les données

        # Styles pour les boutons
        save_button.setStyleSheet("background-color: #67B667; font-size: 16px; color: white; border-radius: 5px; padding: 5px 15px 5px 15px;")
        cancel_button.setStyleSheet("background-color: #F02B3D; font-size: 16px; color: white; border-radius: 5px; padding: 5px 15px 5px 15px;")
        
        # Alignement à droite des boutons
        button_layout.addStretch()  # Ajoute un espace élastique pour pousser les boutons à droite
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Ajouter les boutons au layout principal
        layout.addLayout(button_layout)

        # Appliquer le layout principal
        self.setLayout(layout)

    def enregistrer_pays(self):
        """Action pour enregistrer le pays"""
        
        
        # Vérification de la session utilisateur
        self.session_manager = SessionManager()  # Créer une instance de SessionManager
        self.admin_global = self.session_manager.load_session()  # Charger la session
        self.admin_data = self.admin_global.get("admin", {})
        
        nom = self.nom_pays.text()
        code = self.code_pays.text()
        
        if not all([nom, code]):
            QMessageBox.warning(self, "Erreur", "Tous les champs sont obligatoires.")
            return

        # Préparer les données à envoyer à l'API
        account_data = {
            "nom": nom,
            "code": code,
            "id_admin": self.admin_data.get('id_admin')
        }
        
        
        # Ajouter le suffixe /nouveau-pays à l'URL de l'API
        response = requests.post(f"{get_api_url()}/nouveau-pays", account_data)  # Remplace par l'endpoint correct de l'API
         
        if response.status_code == 200:
            data = response.json()
            # Si le code est succes
            if data.get('code') == 200:
                
                QMessageBox.information(self, data.get('message'), data.get('description'))
                        
                # Émettre le signal pour informer la fenêtre principale
                self.pays_enregistre.emit()
                self.accept()  # Fermer la fenêtre
                
            else:
                # Afficher une boîte de message d'avertissement si l'API répond avec un code d'erreur
                QMessageBox.warning(self, "Erreur", data.get('description'))
        else:
            # En cas d'erreur de l'API
            QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API ou d'obtenir les administrateurs.")

