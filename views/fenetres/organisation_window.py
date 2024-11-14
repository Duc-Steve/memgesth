from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog
from PySide6.QtCore import Qt
from config.image_path import ImagePath  # Importation de la classe de configuration du logo

# Fenêtre pour le Tableau de Bord
class OrganisationWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Organisation")
        self.setFixedSize(1200, 650)
        
        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())
        
        # Créer un layout vertical pour le dialogue
        layout = QVBoxLayout()
        
        label = QLabel("Bienvenue sur la page Organisation", self)
        label.setAlignment(Qt.AlignCenter)
        
        # Ajouter le label au layout
        layout.addWidget(label)
        
        # Appliquer le layout au QDialog
        self.setLayout(layout)
