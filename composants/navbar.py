from PySide6.QtWidgets import QWidget, QMenuBar, QMenu, QVBoxLayout
from PySide6.QtGui import QAction, QIcon

class Navbar(QWidget):
    def __init__(self):
        super().__init__()

        # Fixer la hauteur du widget Navbar à 50px
        self.setFixedHeight(33)
        
        # Créer la barre de menu qui va ressembler à celle d'Adobe Photoshop
        self.menu_bar = QMenuBar(self)

        # Appliquer un style à la barre de menu
        self.menu_bar.setStyleSheet(""" 
            QMenuBar {
                background-color: #121F91;  /* Fond de la barre de menu */
                color: white;  /* Couleur du texte */
                padding: 5px;  /* Espacement interne */
                border-radius: 5px;
            }
            QMenuBar::item {
                background: transparent;  /* Transparent au départ */
                padding: 3px 20px;  /* Espacement autour du texte */
            }
            QMenuBar::item:selected {
                background-color: #F02B3D;  /* Changement de couleur au survol */
            }
            QMenu {
                background-color: #FFFFFF;  /* Fond du menu déroulant */
                color: #121F91;  /* Texte des items */
            }
            QMenu::item:selected {
                background-color: #67B667;  /* Couleur des items sélectionnés */
            }
        """)

        # Créer les menus "Menu", "Raccourci" et "Aide"
        menu = self.menu_bar.addMenu("Menu")
        raccourci = self.menu_bar.addMenu("Raccourcis")
        aide = self.menu_bar.addMenu("Aide")

        # Ajouter des actions pour "Menu"
        option1_action = QAction(QIcon("assets/icons/add.png"), "Informations", self)
        option1_action.triggered.connect(self.open_information_window)  # Connexion à la méthode pour ouvrir la fenêtre
        option2_action = QAction(QIcon("assets/icons/add.png"), "Importation", self)
        option3_action = QAction(QIcon("assets/icons/add.png"), "Exportation", self)
        option4_action = QAction(QIcon("assets/icons/add.png"), "Configuration", self)
        menu.addAction(option1_action)
        menu.addAction(option2_action)
        menu.addAction(option3_action)
        menu.addAction(option4_action)

        # Ajouter des actions pour "Raccourcis"
        raccourci_action1 = QAction(QIcon("assets/icons/add.png"), "Enregistrer un(e) élève", self)
        # raccourci_action1.triggered.connect(self.open_nouvel_eleve_window)  # Connexion à la méthode pour ouvrir la fenêtre
        raccourci_action2 = QAction(QIcon("assets/icons/add.png"), "Nouvelle année", self)
        raccourci.addAction(raccourci_action1)
        raccourci.addAction(raccourci_action2)

        # Ajouter des actions pour "Aide"
        aide_action1 = QAction(QIcon("assets/icons/add.png"), "Supports", self)
        aide_action2 = QAction(QIcon("assets/icons/add.png"), "À propos", self)
        aide.addAction(aide_action1)
        aide.addAction(aide_action2)

        # Créer un layout pour y ajouter la barre de menu
        layout = QVBoxLayout()
        layout.addWidget(self.menu_bar)

        # Retirer les marges externes du layout
        layout.setContentsMargins(0, 0, 0, 0) 
         

        # Appliquer le layout au widget
        self.setLayout(layout)
        
        
    # Méthode pour ouvrir la fenêtre de configuration
    def open_information_window(self):
        from views.fenetres.information_organisation_window import InformationOrganisationWindow
        self.config_window = InformationOrganisationWindow()  # Créer une instance de la fenêtre de configuration
        self.config_window.exec_()  # Afficher la fenêtre en mode modal
            
            

# Assurez-vous que le parent de Navbar n'applique pas de marges
