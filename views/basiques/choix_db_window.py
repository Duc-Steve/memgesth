# views/basiques/choix_db_window.py

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QRadioButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from views.basiques.configuration_ligne_window import ConfigurationLigneWindow  # Importation de la fenêtre de configuration
from config.image_path import ImagePath  # Pour obtenir l'icône
from views.basiques.configuration_local_window import ConfigurationLocalWindow  # Importation de la fenêtre de configuration local
import json

# Nom des fichiers de configuration JSON
CONFIG_FILE = "config.json"

# Classe principale pour la fenêtre de choix
class ChoixDbWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        # Définir le titre et l'icône de la fenêtre
        self.setWindowTitle("Choix de base de donnée")
        self.setWindowIcon(ImagePath.get_icon())

        # Créer le layout principal
        layout = QVBoxLayout()

        # Ajouter les options de base de données
        self.radio_en_ligne = QRadioButton("Option en ligne")
        self.radio_locale = QRadioButton("Option locale")

        # Par défaut, sélectionner l'option ligne
        self.radio_en_ligne.setChecked(True)

        # Ajouter les radios au layout
        layout.addWidget(QLabel("Choisissez une option de base de données :"))
        layout.addWidget(self.radio_en_ligne)
        layout.addWidget(self.radio_locale)

        # Ajouter le bouton Valider
        self.valider_button = QPushButton("Valider")
        self.valider_button.clicked.connect(self.valider_choix)
        self.valider_button.setStyleSheet(
            "background-color: #121F91; color: #FFFFFF; font-size: 18px; padding: 5px 10px; border-radius: 8px; margin-top: 15px"
        )
        layout.addWidget(self.valider_button)

        # Créer un widget central pour le layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def valider_choix(self):
        choix_db = "local" if self.radio_locale.isChecked() else "ligne"

        # Enregistrer le choix dans le fichier de configuration
        self.enregistrer_choix(choix_db)

        # Rediriger vers la fenêtre appropriée
        if choix_db == "ligne":
            self.ouvrir_fenetre(ConfigurationLigneWindow)
        else:
            self.ouvrir_fenetre(ConfigurationLocalWindow)

    def enregistrer_choix(self, choix):
        try:
            with open(CONFIG_FILE, 'r+') as file:
                config = json.load(file)
                config["choix_localisation_db"] = choix
                file.seek(0)
                json.dump(config, file, indent=4)
                file.truncate()
        except FileNotFoundError:
            with open(CONFIG_FILE, 'w') as file:
                json.dump({"choix_localisation_db": choix}, file, indent=4)

    def ouvrir_fenetre(self, fenetre_class):
        self.hide()  # Cacher la fenêtre actuelle
        self.nouvelle_fenetre = fenetre_class()
        self.nouvelle_fenetre.show()
