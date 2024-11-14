from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class Footer(QWidget):
    def __init__(self):
        super().__init__()

        # Fixer la hauteur du footer à 30px (vous pouvez ajuster cette valeur)
        self.setFixedHeight(30)

        # Créer un layout pour le footer
        layout = QVBoxLayout()

        # Créer un label pour le footer
        footer_label = QLabel("AMOSAG-Consulting - © 2024 Memgesth", self)
        
        # Centrer le texte du label
        footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Appliquer le style pour la couleur de fond, padding et largeur
        footer_label.setStyleSheet("""
            background-color: #121F91;  /* Couleur de fond */
            padding: 5px;               /* Padding autour du contenu */
            width: 100%;                /* Prendre toute la largeur disponible */
            color: white;
            border-radius: 5px;
        """)

        # Ajouter le label au layout
        layout.addWidget(footer_label)

        # Retirer les marges externes du layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Appliquer le layout au widget
        self.setLayout(layout)
