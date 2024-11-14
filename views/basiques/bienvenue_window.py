from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
# Interface/avancee/welcome.py
from views.basiques.choix_db_window import ChoixDbWindow  # Notez la casse ici
from config.image_path import ImagePath  # Pour obtenir l'icône


# Classe principale pour la fenêtre d'accueil
class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Définir le titre et l'icône de la fenêtre
        self.setWindowTitle("Bienvenue à Memgesth")
        self.setWindowIcon(ImagePath.get_icon())

        # Définir la taille de la fenêtre
        self.setFixedSize(600, 500)

        # Créer un layout vertical
        layout = QVBoxLayout()

        # Ajouter le logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap("assets/images/logoMemgesth.png")
        self.logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Message de bienvenue
        self.welcome_label = QLabel("Bienvenue à Memgesth")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #174140; margin-top: 20px")
        layout.addWidget(self.welcome_label)

        # Phrase d'introduction
        self.message_label = QLabel(
            "Memgesth, votre solution complète pour la gestion partielle de votre organisation."
        )
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("font-size: 16px; color: #174140; margin-bottom: 20px")
        layout.addWidget(self.message_label)

        # Bouton "Commencer"
        self.start_button = QPushButton("Commencer")
        self.start_button.setStyleSheet(
            "background-color: #121F91; color: #FFFFFF; font-size: 18px; padding: 10px 20px; border-radius: 8px;"
        )
        layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.allez_choix_db_window)  

        # Centrer les éléments
        layout.setAlignment(Qt.AlignCenter)

        # Créer un widget central et lui appliquer le layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def allez_choix_db_window(self):
        """Fonction pour rediriger vers la fenêtre de configuration"""
        self.hide()  # Cacher la fenêtre actuelle
        self.choix_db_window = ChoixDbWindow(self)  # Passer l'instance courante en tant que parent à ChoixDbWindow
        self.choix_db_window.show()
