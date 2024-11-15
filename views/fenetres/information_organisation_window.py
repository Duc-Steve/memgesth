from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QLineEdit, QFileDialog, QMessageBox, QInputDialog, QAbstractScrollArea
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtCore import QSize
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
import pandas as pd
from fpdf import FPDF
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt  # Importer Qt pour utiliser AspectRatioMode
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from views.fenetres.nouvelle_information_window import NouvelleInformationWindow
from services.configuration_manager import get_api_url
import requests  # Importation de la bibliothèque requests pour faire des requêtes HTTP
from functools import partial
import urllib.request


# Classe pour la fenêtre de configuration
class InformationOrganisationWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Information Pays")
        self.setFixedSize(1200, 650)
        
        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())
        
        
        # Créer un layout vertical pour le dialogue
        main_layout = QVBoxLayout()
        
        # Créer un layout horizontal pour le text
        text_layout = QHBoxLayout()
        
        # Titre
        text_layout = QLabel("INFORMATION PAYS")
        text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_layout.setStyleSheet("font-size: 16px; margin-bottom: 15px; background-color: #121F91; color: white; border-radius: 5px; padding: 5px;")

        # Créer un layout horizontal pour les boutons en haut
        top_button_layout = QHBoxLayout()
        top_button_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        
        # Ajout du bouton d'enregistrement du pays
        add_button = QPushButton("Nouvelle information")
        add_button.setStyleSheet("margin-bottom: 15px; font-size: 16px; background-color: #67B667; color: white; padding: 10px; border-radius: 5px;")
        add_button.clicked.connect(self.ouvrir_nouvelle_information)
        top_button_layout.addWidget(add_button)

        # Ajouter les boutons d'impression et d'exportation
        export_button = QPushButton("Exporter")
        export_button.setStyleSheet("margin-bottom: 15px; padding: 10px; font-size: 14px; background-color: #121F91; color: white; border-radius: 5px;")
        export_button.clicked.connect(self.show_export_options)
        top_button_layout.addWidget(export_button)
        
        rafraichir_button = QPushButton()
        rafraichir_button.setIcon(QIcon("assets/icons/refresh.png"))  # Chemin de l'icône de déconnexion
        rafraichir_button.setIconSize(QSize(40, 40))  # Définir la taille de l'icône (ajustez les dimensions selon vos besoins)
        rafraichir_button.setStyleSheet("margin-bottom: 15px; padding: 10px; font-size: 14px; background-color: white; color: #121F91; border-radius: 5px; border: 2px solid #121F91")
        rafraichir_button.clicked.connect(self.populate_table)
        # Connexion de l'action du bouton des donnees de la table ici
        top_button_layout.addWidget(rafraichir_button)
        
        # Ajouter le layout text au layout principale
        main_layout.addWidget(text_layout)

        # Ajouter le layout des boutons au layout principal
        main_layout.addLayout(top_button_layout)


        # Ajouter une barre de recherche et les filtres
        filter_layout = QHBoxLayout()

        # Barre de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.search_input.textChanged.connect(self.update_table_data)
        filter_layout.addWidget(self.search_input)

        main_layout.addLayout(filter_layout)
        
        # Créer le tableau avec 6 colonnes (le nombre de lignes sera ajusté dynamiquement)
        self.table = QTableWidget(0, 6, self)  # Initialisation avec 0 lignes
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Définir les titres des colonnes
        column_titles = [
            "Modifier",
            "Lien de l'Image",
            "Date de Création",
            "Date Mise à jour",
            "Nom de l'Information",
            "Nom du Pays",
            "Nom de l'Administrateur",
            "Email de l'Administrateur",
            "Email de l'Information",
            "Contact 1",
            "Contact 2",
            "Fixe",
            "Boîte Postale",
            "RCCM",
            "IFU",
            "Localisation",
            "Slogan",
            "Pied de Description"
        ]
        
        # Appliquer le style de l'en-tête du tableau
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #F02B3D; 
                color: white; 
                font-size: 14px; 
                padding: 5px;
                border: 1px solid #121F91;
            }
        """)

        
        self.table.setColumnCount(len(column_titles))  # Définir le nombre de colonnes

        # Appliquer les titres des colonnes
        self.table.setHorizontalHeaderLabels(column_titles)
        

        # Exemple d'ajout de contenu aux lignes
        self.populate_table()

        # Ajouter le tableau au layout principal
        main_layout.addWidget(self.table)

        # Appliquer le layout au QDialog
        self.setLayout(main_layout)
        
   
        
    def mettre_a_jour_tableau(self):
        """Mettre à jour le tableau avec les nouveaux informations"""
        # Cette méthode devrait recharger les données de l'API et mettre à jour le tableau
        self.populate_table()

    def populate_table(self):
        """Remplir le tableau avec des données et des boutons d'action"""

        # Récupérer la liste des informations depuis l'API
        response = requests.get(f"{get_api_url()}/liste-information")  # Assurez-vous que l'endpoint est correct

        if response.status_code == 200:
            data = response.json()
            
            # Vérifier si la réponse contient un code de succès
            if data.get('code') == 200:
                # Remplir les données de la liste dans le tableau
                information_list = data.get('information', [])  # Supposer que la clé 'information' contient la liste des informations

                # Ajuster le nombre de lignes en fonction des données reçues
                self.table.setRowCount(len(information_list))

                for row, information in enumerate(information_list):
                    # Créer un layout pour les actions (boutons)
                    action_layout = QHBoxLayout()

                    # Ajouter un bouton d'édition
                    edit_button = QPushButton()
                    edit_button.setIcon(QIcon("assets/icons/edit.png"))
                    edit_button.setStyleSheet("background-color: none; border-radius: 5px;")
                    action_layout.addWidget(edit_button)

                    # Créer un widget pour contenir les boutons
                    action_widget = QWidget()
                    action_widget.setLayout(action_layout)

                    # Ajouter un bouton transparent pour capturer tous les clics sur le widget
                    click_button = QPushButton(action_widget)
                    click_button.setStyleSheet("background-color: transparent; border: none;")
                    click_button.setGeometry(0, 0, action_widget.width(), action_widget.height())
                    click_button.raise_()  # Assurez-vous que le bouton est au-dessus des autres éléments

                    # Ajouter le widget d'action à la table dans la cellule appropriée
                    self.table.setCellWidget(row, 0, action_widget)

                    # Ajouter un bouton de téléchargement dans la cellule
                    download_layout = QHBoxLayout()

                    # Créer le bouton de téléchargement
                    download_button = QPushButton()
                    download_button.setIcon(QIcon("assets/icons/download.png"))  # Remplacez par l'icône de téléchargement
                    download_button.setStyleSheet("background-color: none; border-radius: 5px;")
                    download_layout.addWidget(download_button)

                    # Créer un widget pour contenir le bouton de téléchargement
                    download_widget = QWidget()
                    download_widget.setLayout(download_layout)

                    # Ajouter un bouton transparent pour capturer les clics sur l'ensemble du widget
                    click_download = QPushButton(download_widget)
                    click_download.setStyleSheet("background-color: transparent; border: none;")

                    # Placer le bouton transparent sur toute la surface du widget
                    click_download.setGeometry(0, 0, download_widget.width(), download_widget.height())
                    click_download.raise_()  # Assurez-vous que le bouton est au-dessus des autres éléments

                    # Connecter le bouton de téléchargement à une fonction
                    lienImage = information.get('enteteLienImage')  # Récupérer le lien de l'image depuis les informations
                    click_download.clicked.connect(partial(self.on_download_clicked, lienImage))

                    # Ajouter le widget de téléchargement à la cellule du tableau
                    self.table.setCellWidget(row, 1, download_widget)

                    # Ajouter d'autres informations dans la table (colonnes supplémentaires)
                    self.table.setItem(row, 2, QTableWidgetItem(information.get('dateCreation')))  # Date de création
                    self.table.setItem(row, 3, QTableWidgetItem(information.get('dateMiseJour')))  # Date de mise à jour
                    self.table.setItem(row, 4, QTableWidgetItem(information.get('nomInfo')))  # Nom de l'information
                    self.table.setItem(row, 5, QTableWidgetItem(information.get('nomPays')))  # Nom du pays
                    self.table.setItem(row, 6, QTableWidgetItem(information.get('nomAdmin')))  # Nom de l'administrateur
                    self.table.setItem(row, 7, QTableWidgetItem(information.get('emailAdmin')))  # Email de l'administrateur
                    self.table.setItem(row, 8, QTableWidgetItem(information.get('email')))  # Email de l'information
                    self.table.setItem(row, 9, QTableWidgetItem(information.get('contactUn')))  # Contact 1
                    self.table.setItem(row, 10, QTableWidgetItem(information.get('contactDeux')))  # Contact 2
                    self.table.setItem(row, 11, QTableWidgetItem(information.get('fixe')))  # Fixe
                    self.table.setItem(row, 12, QTableWidgetItem(information.get('boitePostale')))  # Boîte postale
                    self.table.setItem(row, 13, QTableWidgetItem(information.get('rccm')))  # RCCM
                    self.table.setItem(row, 14, QTableWidgetItem(information.get('ifu')))  # IFU
                    self.table.setItem(row, 15, QTableWidgetItem(information.get('localisation')))  # Localisation
                    self.table.setItem(row, 16, QTableWidgetItem(information.get('slogan')))  # Slogan
                    self.table.setItem(row, 17, QTableWidgetItem(information.get('piedDescription')))  # Pied de description

                    # Désactiver l'édition des cellules sauf pour la colonne d'actions
                    for col in range(1, 6):
                        item = self.table.item(row, col)
                        if item:
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                                                
                # Ajuster la taille des colonnes en fonction du contenu
                self.table.resizeColumnsToContents()

            else:
                # Afficher une boîte de message d'avertissement si l'API répond avec un code d'erreur
                QMessageBox.warning(self, "Erreur", data.get('message', 'Erreur inconnue de l\'API'))
        else:
            # Gérer les erreurs de connexion à l'API
            QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API ou d'obtenir la liste des informations.")


    # Fonction pour télécharger le fichier à partir du lien
    def on_download_clicked(self, lienImage):
        try:
            # Ouvrir une boîte de dialogue pour demander à l'utilisateur où enregistrer le fichier
            options = QFileDialog.Options()
            # Demander à l'utilisateur de choisir le nom et l'emplacement pour enregistrer l'image
            file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer l'image sous...", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)

            if file_name:
                # Si l'utilisateur a choisi un nom de fichier, télécharger l'image
                urllib.request.urlretrieve(lienImage, file_name)
                QMessageBox.information(self, "Succès", "Le fichier a été téléchargé avec succès.")
            else:
                # Si l'utilisateur annule la boîte de dialogue, afficher un message d'annulation
                QMessageBox.warning(self, "Annulation", "Le téléchargement a été annulé.")
        except Exception as e:
            print(f"Erreur de téléchargement : {e}")
            QMessageBox.warning(self, "Erreur", f"Une erreur est survenue pendant le téléchargement : {e}")
            

    def update_table_data(self):
        search_text = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            text_match = any(search_text in (self.table.item(row, col).text().lower() if self.table.item(row, col) else "") for col in range(self.table.columnCount()))

            if text_match:
                self.table.showRow(row)
            else:
                self.table.hideRow(row)


    def show_export_options(self):
        """Afficher les options d'exportation pour Excel ou PDF"""
        options = ["Excel", "PDF"]
        selected_option, ok = QInputDialog.getItem(self, "Choisir le format", "Format d'exportation :", options, 0, False)
        
        if ok and selected_option:
            if selected_option == "Excel":
                self.export_to_excel()
            elif selected_option == "PDF":
                self.export_to_pdf()


    def export_to_excel(self):
        """Exporter les données du tableau en fichier Excel"""
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier Excel", "", "Fichiers Excel (*.xlsx)")
        if not path:
            return

        data = []
        # Récupérer les titres des colonnes
        headers = [self.table.horizontalHeaderItem(col).text() for col in range(self.table.columnCount())]
        headers = headers[2:]  # Supprimer les deux premiers titres

        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

        # Créer un DataFrame avec pandas
        df = pd.DataFrame(data, columns=headers)
        try:
            df.to_excel(path, index=False)
            QMessageBox.information(self, "Exportation réussie", f"Le fichier a été exporté avec succès à l'emplacement : {path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation : {str(e)}")   


    def export_to_pdf(self):
        """Exporter les données du tableau en fichier PDF avec orientation dynamique"""
        QMessageBox.information(self, "Désactiver", "Action désactiver") 
         

        
    def ouvrir_nouvelle_information(self):
        """Afficher la fenêtre NouvelleInformationWindow lorsque le bouton est cliqué"""
        # Créer une instance de NouvelleInformationWindow
        self.nouvelle_information_window = NouvelleInformationWindow(self)
        # Connecter le signal à la méthode pour mettre à jour le tableau
        self.nouvelle_information_window.information_enregistre.connect(self.mettre_a_jour_tableau)
        self.nouvelle_information_window.exec()  # Utilisez exec() pour ouvrir la fenêtre comme une boîte de dialogue modale

        