from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QLineEdit, QFileDialog, QMessageBox, QInputDialog, QAbstractScrollArea
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPainter
from PySide6.QtCore import QSize
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
import pandas as pd
from fpdf import FPDF
from views.fenetres.nouveau_pays_window import NouveauPaysWindow
from services.configuration_manager import get_api_url
import requests  # Importation de la bibliothèque requests pour faire des requêtes HTTP
from functools import partial




# Fenêtre pour le Tableau de Bord
class PaysInstallerWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Gestion des pays")
        self.setFixedSize(1200, 650)
        
        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())
        
        
        # Créer un layout vertical pour le dialogue
        main_layout = QVBoxLayout()
        
        # Créer un layout horizontal pour le text
        text_layout = QHBoxLayout()
        
        # Titre
        text_layout = QLabel("GESTION DES PAYS")
        text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_layout.setStyleSheet("font-size: 16px; margin-bottom: 15px; background-color: #121F91; color: white; border-radius: 5px; padding: 5px;")

        # Créer un layout horizontal pour les boutons en haut
        top_button_layout = QHBoxLayout()
        top_button_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        
        # Ajout du bouton d'enregistrement du pays
        add_button = QPushButton("Nouveau pays")
        add_button.setStyleSheet("margin-bottom: 15px; font-size: 16px; background-color: #67B667; color: white; padding: 10px; border-radius: 5px;")
        add_button.clicked.connect(self.ouvrir_nouveau_pays)
        top_button_layout.addWidget(add_button)

        # Ajouter les boutons d'impression et d'exportation
        export_button = QPushButton("Exporter")
        export_button.setStyleSheet("margin-bottom: 15px; padding: 10px; font-size: 14px; background-color: #121F91; color: white; border-radius: 5px;")
        export_button.clicked.connect(self.show_export_options)
        top_button_layout.addWidget(export_button)

        print_button = QPushButton("Imprimer")
        print_button.setStyleSheet("margin-bottom: 15px; padding: 10px; font-size: 14px; background-color: #121F91; color: white; border-radius: 5px;")
        print_button.clicked.connect(self.print_table)
        # Connexion de l'action du bouton d'impression ici
        top_button_layout.addWidget(print_button)
        
        
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

        # Filtre de statut
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Tous", "actif", "inactif"])
        self.status_combo.currentTextChanged.connect(self.update_table_data)
        filter_layout.addWidget(self.status_combo)

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
            "Action", "Date de Création", "Date Mise à jour", "Nom Pays", "Code Pays", "Statut"
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
        """Mettre à jour le tableau avec les nouveaux pays"""
        # Cette méthode devrait recharger les données de l'API et mettre à jour le tableau
        self.populate_table()


    def populate_table(self):
        """Remplir le tableau avec des données et des boutons d'action"""

        # Récupérer la liste des pays depuis l'API
        response = requests.get(f"{get_api_url()}/liste-pays")  # Assurez-vous que l'endpoint est correct

        if response.status_code == 200:
            data = response.json()
            
            # Vérifier si la réponse contient un code de succès
            if data.get('code') == 200:
                # Remplir les données de la liste dans le tableau
                pays_list = data.get('pays', [])  # Supposer que la clé 'pays' contient la liste des pays

                # Ajuster le nombre de lignes en fonction des données reçues
                self.table.setRowCount(len(pays_list))

                for row, pays in enumerate(pays_list):
                    action_layout = QHBoxLayout()

                    # Si le pays est actif
                    if pays.get('statutPays') == "actif":
                        delete_button = QPushButton()
                        delete_button.setIcon(QIcon("assets/icons/delete.png"))
                        delete_button.setStyleSheet("background-color: none; border-radius: 5px;")
                        action_layout.addWidget(delete_button)

                    # Sinon
                    else:
                        add_button = QPushButton()
                        add_button.setIcon(QIcon("assets/icons/add2.png"))
                        add_button.setStyleSheet("background-color: none; border-radius: 5px;")
                        action_layout.addWidget(add_button)

                    action_widget = QWidget()
                    action_widget.setLayout(action_layout)

                    # Ajouter un bouton transparent sur l'ensemble du widget pour capturer les clics
                    click_button = QPushButton(action_widget)
                    click_button.setStyleSheet("background-color: transparent; border: none;")
                    click_button.clicked.connect(partial(self.change_statut_country, pays.get('idPays')))

                    # Placer le bouton sur toute la surface du widget
                    click_button.setGeometry(0, 0, action_widget.width(), action_widget.height())
                    click_button.raise_()  # Assurez-vous que le bouton est au-dessus des autres éléments

                    # Ajouter le widget d'action à la table
                    self.table.setCellWidget(row, 0, action_widget)

                    # Ajouter les données de chaque pays dans le tableau
                    self.table.setItem(row, 1, QTableWidgetItem(pays.get('dateCreation')))  # Date de création
                    self.table.setItem(row, 2, QTableWidgetItem(pays.get('dateMiseJour')))  # Date de mise à jour
                    self.table.setItem(row, 3, QTableWidgetItem(pays.get('nom')))  # Nom du pays
                    self.table.setItem(row, 4, QTableWidgetItem(pays.get('code')))  # Code du pays
                    self.table.setItem(row, 5, QTableWidgetItem(pays.get('statutPays')))  # Statut

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
            QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API ou d'obtenir la liste des pays.")


    def change_statut_country(self, idPays):
        """Remplir le tableau avec des données et des boutons d'action"""

        # Récupérer la liste des pays depuis l'API
        response = requests.get(f"{get_api_url()}/statut-pays/{idPays}")  # Assurez-vous que l'endpoint est correct

        if response.status_code == 200:
            data = response.json()
            
            # Vérifier si la réponse contient un code de succès
            if data.get('code') == 202:
                QMessageBox.information(self, data.get('message'), data.get('description'))
                        
                # Cette méthode devrait recharger les données de l'API et mettre à jour le tableau
                self.populate_table()
            else:
                # Afficher une boîte de message d'avertissement si l'API répond avec un code d'erreur
                QMessageBox.warning(self, "Erreur", data.get('description'))
        else:
            # Gérer les erreurs de connexion à l'API
            QMessageBox.warning(self, "Erreur API", "Impossible de se connecter à l'API ou d'obtenir la liste des pays.")
                

    def update_table_data(self):
        filter_status = self.status_combo.currentText()
        search_text = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            status_match = (filter_status == "Tous" or self.table.item(row, 5).text() == filter_status)
            text_match = any(search_text in (self.table.item(row, col).text().lower() if self.table.item(row, col) else "") for col in range(self.table.columnCount()))

            if status_match and text_match:
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
        headers = headers[1:]  # Supprimer le premier titre

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
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier PDF", "", "Fichiers PDF (*.pdf)")
        if not path:
            return

        # Déterminer le nombre de colonnes
        num_columns = self.table.columnCount()
        
        # Exemple avec 6 colonnes, ajustez les valeurs pour chaque colonne
        column_widths = [20, 50, 50, 100, 40, 20]  # Largeur de chaque colonne en mm

        # Vérification pour s'assurer que le nombre de colonnes et la taille des colonnes correspondent
        if len(column_widths) != num_columns:
            # Si les largeurs définies ne correspondent pas au nombre de colonnes, utiliser une largeur uniforme
            cell_width = 280 / num_columns  # Largeur répartie uniformément pour l'orientation paysage
            column_widths = [cell_width] * num_columns  # Appliquer cette largeur à toutes les colonnes

        # Créer le PDF avec orientation paysage
        orientation = 'L'  # Orientation paysage
        pdf = FPDF(orientation, 'mm', 'A4')
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)

        # Ajouter un titre
        pdf.cell(0, 10, "Liste des pays", 0, 1, 'C')

        # Récupérer les titres des colonnes depuis l'en-tête de la table
        column_titles = [self.table.horizontalHeaderItem(col).text() for col in range(num_columns)]
        
        # Ajouter les titres des colonnes
        pdf.set_font("Arial", 'B', 12)
        for i, title in enumerate(column_titles):
            pdf.cell(column_widths[i], 10, title, 1, 0, 'C')
        pdf.ln()

        # Ajouter les données du tableau
        pdf.set_font("Arial", '', 12)
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                for col in range(num_columns):
                    item = self.table.item(row, col)
                    pdf.cell(column_widths[col], 10, item.text() if item else "", 1)
                pdf.ln()

        # Enregistrer le fichier PDF
        try:
            pdf.output(path)
            QMessageBox.information(self, "Exportation réussie", f"Le fichier PDF a été exporté avec succès à l'emplacement : {path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur s'est produite lors de l'exportation : {str(e)}")  
         
            
    def print_table(self):
        """Imprimer les données du tableau"""
        printer = QPrinter(QPrinter.HighResolution)

        # Configurer la boîte de dialogue d'impression
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QPrintDialog.Rejected:
            return  # L'utilisateur a annulé l'impression

        # Démarrer l'impression
        painter = QPainter(printer)

        # Définir la taille de la page et de la table pour l'impression
        page_rect = printer.pageRect()
        table_rect = self.table.geometry()

        scale_x = page_rect.width() / table_rect.width()
        scale_y = page_rect.height() / table_rect.height()

        painter.scale(min(scale_x, scale_y), min(scale_x, scale_y))

        # Dessiner le contenu du tableau sur la page
        self.table.render(painter)
        painter.end()


    def ouvrir_nouveau_pays(self):
        """Afficher la fenêtre NouveauPaysWindow lorsque le bouton est cliqué"""
        # Créer une instance de NouveauPaysWindow
        self.nouveau_pays_window = NouveauPaysWindow(self)
        # Connecter le signal à la méthode pour mettre à jour le tableau
        self.nouveau_pays_window.pays_enregistre.connect(self.mettre_a_jour_tableau)
        self.nouveau_pays_window.exec()  # Utilisez exec() pour ouvrir la fenêtre comme une boîte de dialogue modale

        