from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt  # Importer Qt pour utiliser AspectRatioMode
from config.image_path import ImagePath  # Importation de la classe de configuration du logo


# Classe pour la fenêtre de configuration
class InformationOrganisationWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information organisation")
        self.setFixedSize(850, 600)  # Définir la taille de la fenêtre
        
        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())

        layout = QVBoxLayout()

        # Partie 1 : En tête des fichers
        header_layout = QVBoxLayout()

        # Titre de la Partie 1
        header_title = QLabel("EN TETE DES FICHIERS")
        header_title.setStyleSheet("margin-top: 5px; background-color: #121F91; color: white; border-radius: 5px; padding: 5px;")
        header_layout.addWidget(header_title)

        # Afficher l'image choisie
        self.image_label = QLabel("Aucune image choisie")  # Label pour afficher le nom de l'image
        header_layout.addWidget(self.image_label)

        # Input image et bouton pour choisir une image
        image_layout = QVBoxLayout()
        select_image_button = QPushButton("Choisir une image")
        select_image_button.clicked.connect(self.choose_image)
        image_layout.addWidget(select_image_button)

        # Textarea pour la saisie
        self.header_text_area = QTextEdit()
        self.header_text_area.setPlaceholderText("Saisir la description ici...")
        image_layout.addWidget(self.header_text_area)

        header_layout.addLayout(image_layout)

        # Partie 2 : INFORMATIONS DE L'ORGANISATION
        school_info_layout = QVBoxLayout()  # Utiliser un QVBoxLayout pour la disposition générale
        school_info_title = QLabel("INFORMATIONS DE L'ORGANISATION")
        school_info_title.setStyleSheet("margin-top: 5px; background-color: #121F91; color: white; border-radius: 5px; padding: 5px;")
        school_info_layout.addWidget(school_info_title)

        school_info_inner_layout = QHBoxLayout()  # Utiliser un QHBoxLayout pour la disposition gauche/droite

        # Section gauche
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Nom:"))
        left_layout.addWidget(QLineEdit())
        left_layout.addWidget(QLabel("Email:"))
        left_layout.addWidget(QLineEdit())
        left_layout.addWidget(QLabel("Contact 1:"))
        left_layout.addWidget(QLineEdit())
        left_layout.addWidget(QLabel("Contact 2:"))
        left_layout.addWidget(QLineEdit())
        left_layout.addWidget(QLabel("Fixe:"))
        left_layout.addWidget(QLineEdit())

        # Section droite
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Boîte postale:"))
        right_layout.addWidget(QLineEdit())
        right_layout.addWidget(QLabel("RCCM:"))
        right_layout.addWidget(QLineEdit())
        right_layout.addWidget(QLabel("IFU:"))
        right_layout.addWidget(QLineEdit())
        right_layout.addWidget(QLabel("Localisation:"))
        right_layout.addWidget(QLineEdit())
        right_layout.addWidget(QLabel("Slogan:"))
        right_layout.addWidget(QLineEdit())

        # Ajouter les sections gauche et droite à la mise en page
        school_info_inner_layout.addLayout(left_layout)
        school_info_inner_layout.addLayout(right_layout)
        school_info_layout.addLayout(school_info_inner_layout)

        # Créer une mise en page principale pour les deux groupes
        main_layout = QHBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addLayout(school_info_layout)

        layout.addLayout(main_layout)

        # Partie 3 : Pied de page des fichers
        footer_layout = QVBoxLayout()
        footer_title = QLabel("PIED DES FICHIERS")
        footer_title.setStyleSheet("margin-top: 20px; background-color: #121F91; color: white; border-radius: 5px; padding: 5px;")
        footer_layout.addWidget(footer_title)

        self.footer_text_area = QTextEdit()
        self.footer_text_area.setPlaceholderText("Saisir le pied de page ici...")
        footer_layout.addWidget(self.footer_text_area)

        layout.addLayout(footer_layout)

        # Ajouter les boutons Enregistrer et Annuler
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 30, 0, 0)  # Marges pour le bouton
        cancel_button = QPushButton("Annuler")
        save_button = QPushButton("Enregistrer")
        cancel_button.clicked.connect(self.close)  # Fermer la fenêtre à la demande

        # Styles pour les boutons
        save_button.setStyleSheet("background-color: #67B667; font-size: 16px; color: white; border-radius: 5px; padding: 5px 15px 5px 15px;")
        cancel_button.setStyleSheet("background-color: #F02B3D; font-size: 16px; color: white; border-radius: 5px; padding: 5px 15px 5px 15px;")
        
        # Alignement à droite des boutons
        button_layout.addStretch()  # Ajoute un espace élastique pour pousser les boutons à droite
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def choose_image(self):
        # Ouvrir une boîte de dialogue pour choisir une image
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.image_label.setText(file_name)  # Afficher le chemin de l'image choisie
            self.set_image_preview(file_name)

    def set_image_preview(self, image_path):
        # Mettre à jour l'icône de la fenêtre avec l'image choisie
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))  # Ajuster la taille de l'image
