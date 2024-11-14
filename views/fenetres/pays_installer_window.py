from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QDialog, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QComboBox, QLineEdit, QFileDialog, QMessageBox, QInputDialog
)
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPainter
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
import pandas as pd
from fpdf import FPDF
from views.fenetres.nouveau_pays_window import NouveauPaysWindow


# Fenêtre pour le Tableau de Bord
class PaysInstallerWindow(QDialog):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Gestion des pays")
        self.setFixedSize(850, 650)
        
        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())
        
        
        # Créer un layout vertical pour le dialogue
        main_layout = QVBoxLayout()
        
        # Créer un layout horizontal pour le text
        text_layout = QHBoxLayout()
        
        # Titre
        text_layout = QLabel("GESTION DES PAYS")
        text_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_layout.setStyleSheet("font-size: 16px; margin-bottom: 15px; background-color: #F02B3D; color: white; border-radius: 5px; padding: 5px;")

        # Créer un layout horizontal pour les boutons en haut
        top_button_layout = QHBoxLayout()
        top_button_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)

        # Ajouter le bouton d'enregistrement du pays
        add_button = QPushButton("Enregistrement d'un pays")
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
        
        # Ajouter le layout text au layout principale
        main_layout.addWidget(text_layout)

        # Ajouter le layout des boutons au layout principal
        main_layout.addLayout(top_button_layout)

        # Ajouter une barre de recherche et les filtres
        filter_layout = QHBoxLayout()

        # Filtre de statut
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Tous", "Actif", "Inactif"])
        self.status_combo.currentTextChanged.connect(self.update_table_data)
        filter_layout.addWidget(self.status_combo)

        # Barre de recherche
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Rechercher...")
        self.search_input.textChanged.connect(self.update_table_data)
        filter_layout.addWidget(self.search_input)

        main_layout.addLayout(filter_layout)

        # Créer le tableau avec 10 lignes et 16 colonnes
        self.table = QTableWidget(10, 7, self)
        self.table.showMaximized()

        # Définir les titres des colonnes
        column_titles = [
            "Action", "Date de Création", "Date Mise à jours", "ID", "Nom Pays", "Code Pays", "Statut"
        ] 
        # Appliquer le style de l'en-tête du tableau
        self.table.horizontalHeader().setStyleSheet("background-color: #F02B3D; color: white;")

        # Appliquer les titres des colonnes
        self.table.setHorizontalHeaderLabels(column_titles)
        
        # Appliquer le style de l'en-tête du tableau
        self.table.horizontalHeader().setStyleSheet("background-color: red; color: white;")

        # Exemple d'ajout de contenu aux lignes
        self.populate_table()

        # Ajouter le tableau au layout principal
        main_layout.addWidget(self.table)

        # Appliquer le layout au QDialog
        self.setLayout(main_layout)

    def populate_table(self):
        """Remplir le tableau avec des données fictives et des boutons d'action"""
        for row in range(10):

            action_layout = QHBoxLayout()
            modify_button = QPushButton()
            modify_button.setIcon(QIcon("assets/icons/add.png"))
            modify_button.setStyleSheet("background-color: green; color: white;")
            
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("assets/icons/add.png"))
            delete_button.setStyleSheet("background-color: red; color: white;")

            action_layout.addWidget(modify_button)
            action_layout.addWidget(delete_button)
            action_widget = QWidget()
            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row, 0, action_widget)
            self.table.setItem(row, 1, QTableWidgetItem("01/01/2000"))  # Date de Création
            self.table.setItem(row, 2, QTableWidgetItem("01/09/2023"))  # Date Mise à jours
            self.table.setItem(row, 3, QTableWidgetItem(f"{row + 1}"))  # ID
            self.table.setItem(row, 4, QTableWidgetItem(f"Nom{row + 1}"))  # Nom Pays
            self.table.setItem(row, 5, QTableWidgetItem("Code XYZ "))  # Code Pays
            self.table.setItem(row, 6, QTableWidgetItem("Actif")) # Statut

            # Désactiver l'édition des cellules sauf pour la colonne Action
            for col in range(1, 7):  # Désactive l'édition pour les colonnes 1 à 6
                self.table.item(row, col).setFlags(self.table.item(row, col).flags() & ~Qt.ItemIsEditable)



    def update_table_data(self):
        filter_status = self.status_combo.currentText()
        search_text = self.search_input.text().lower()

        for row in range(self.table.rowCount()):
            status_match = (filter_status == "Tous" or self.table.item(row, 7).text() == filter_status)
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

        # Déterminer l'orientation en fonction du nombre de colonnes
        num_columns = self.table.columnCount()
        orientation = 'P' if num_columns <= 10 else 'L'  # Portrait si <= 10 colonnes, sinon Paysage

        pdf = FPDF(orientation, 'mm', 'A4')
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        
        # Ajouter un titre
        pdf.cell(0, 10, "Liste des élèves", 0, 1, 'C')
        
        # Ajouter les titres des colonnes
        pdf.set_font("Arial", 'B', 12)
        column_titles = [self.table.horizontalHeaderItem(col).text() for col in range(num_columns)]
        
        # Définir la largeur de la cellule en fonction de l'orientation et du nombre de colonnes
        cell_width = 190 / num_columns if orientation == 'P' else 280 / num_columns
        
        for title in column_titles:
            pdf.cell(cell_width, 10, title, 1, 0, 'C')
        pdf.ln()

        # Ajouter les données du tableau
        pdf.set_font("Arial", '', 12)
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                for col in range(num_columns):
                    item = self.table.item(row, col)
                    pdf.cell(cell_width, 10, item.text() if item else "", 1)
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
        """Action pour ouvrir la fenêtre du formulaire d'enregistrement du pays"""
        nouveau_pays = NouveauPaysWindow()
        nouveau_pays.exec_()  # Afficher la fenêtre en mode modal
        
        
        