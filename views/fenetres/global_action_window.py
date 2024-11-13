from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from services.session_manager import SessionManager




# Fenêtre GlobaleAction avec les boutons et leurs actions
class GlobaleActionWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Définir le titre de la fenêtre
        self.setWindowTitle("Globale Action")

        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())

        # Maximiser la fenêtre à l'ouverture
        self.showMaximized()
