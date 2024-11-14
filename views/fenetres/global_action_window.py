from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QSize
from config.image_path import ImagePath  # Importation de la classe de configuration du logo
from services.session_manager import SessionManager
from composants.navbar import Navbar
from views.fenetres.pays_installer_window import PaysInstallerWindow
from views.fenetres.organisation_window import OrganisationWindow






# Fenêtre GlobaleAction avec les boutons et leurs actions
class GlobaleActionWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Définir le titre de la fenêtre
        self.setWindowTitle("Memgesth")

        # Définir l'icône de la fenêtre à partir de la classe ImagePath
        self.setWindowIcon(ImagePath.get_icon())

        # Maximiser la fenêtre à l'ouverture
        self.showMaximized()
        
        # Créer le layout principal
        main_layout = QVBoxLayout()  # Utiliser QVBoxLayout pour empiler la navbar et le contenu
        self.setLayout(main_layout)

        # Ajouter la Navbar en haut
        self.navbar = Navbar()
        main_layout.addWidget(self.navbar)
        
        
        # Vérification de la session utilisateur
        self.session_manager = SessionManager()  # Créer une instance de SessionManager
        self.admin_global = self.session_manager.load_session()  # Charger la session
        self.admin_data = self.admin_global.get("admin", {})
        
        # Ajouter le bloc du nom et du prénom en haut à droite avec l'icône de déconnexion
        user_info_layout = QHBoxLayout()
        user_info_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        user_info_layout.setContentsMargins(0, 0, 0, 0)  # Marges : top=10px, droite alignée

        if self.admin_data:
            # Afficher le nom et le prénom de l'utilisateur
            self.admin_label = QLabel(f"{self.admin_data.get('nom')} {self.admin_data.get('prenom')}")
            self.admin_label.setStyleSheet("font-size: 14px; padding: 5px; margin-right: 1px;")

            # Bouton de déconnexion avec icône
            self.deconnexion_button = QPushButton()
            self.deconnexion_button.setIcon(QIcon("assets/icons/logout.png"))  # Chemin de l'icône de déconnexion
            self.deconnexion_button.setIconSize(QSize(40, 40))  # Définir la taille de l'icône (ajustez les dimensions selon vos besoins)
            self.deconnexion_button.setStyleSheet("border: none; background-color: transparent;")
            self.deconnexion_button.clicked.connect(self.deconnexion)

            # Ajouter le label et le bouton de déconnexion au layout
            user_info_layout.addWidget(self.admin_label)
            user_info_layout.addWidget(self.deconnexion_button)

            # Créer un widget pour contenir le layout et appliquer le style
            user_info_widget = QWidget()
            user_info_widget.setLayout(user_info_layout)
            user_info_widget.setStyleSheet("""
                background-color: white;
                padding: 5px;
                border-radius: 5px;
                margin-top: 8px;
            """)


        else:
            self.ouvrir_connexion()  # Ouvrir la fenêtre de connexion si aucune session n'est chargée

            
        
        # Créer un layout pour le contenu principal (sidebar + boutons)
        content_layout = QHBoxLayout()  # Layout principal horizontal qui contient la sidebar et la section des boutons

        # Créer la sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        # Ajouter le logo de l'application
        self.logo_label = QLabel(self)
        pixmap = QPixmap("assets/images/logoMemgesth.png")
        self.logo_label.setPixmap(pixmap.scaled(175, 175, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(self.logo_label)

        # Liste des libellés des boutons de la sidebar
        sidebar_button_labels = [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Option 5",
            "Option 6",
        ]

        # Ajouter les boutons de la sidebar
        for label in sidebar_button_labels:
            btn = QPushButton(label)
            btn.setStyleSheet(
                "background-color: #67B667; font-size: 16px; padding: 10px; margin: 5px; text-align: left; color: white; border-radius: 5px;"
            )
            sidebar_layout.addWidget(btn)
            
        # Créer un conteneur pour la sidebar et lui assigner le layout
        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(200)  # Largeur de la sidebar

        # Section principale des boutons
        grid_layout = QVBoxLayout()  # Flexbox pour les boutons
        grid_layout.setSpacing(10)  # Espacement entre les boutons
        # Ajouter la section user_info_widget en haut avec un stretch factor de 1 (20% de l'espace)
        grid_layout.addWidget(user_info_widget, 0, Qt.AlignTop | Qt.AlignRight)
        
       
        # Section principale des boutons
        action_layout = QHBoxLayout()  # Flexbox pour les boutons
        action_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        action_layout.setSpacing(10)  # Espacement entre les boutons
        action_layout.setContentsMargins(0, 0, 0, 0)  # Marges : top=10px, droite alignée

        # Liste des libellés de boutons
        button_labels = [
            "Pays Installer", 
            "Organisation", 
        ]

        # Dictionnaire pour stocker les fonctions d'action des boutons
        button_actions = {
            "Pays Installer": self.ouvrir_liste_pays,
            "Organisation": self.ouvrir_organisation,
        }

        # Créer les 8 boutons avec leurs libellés et les connecter à leurs actions
        for label in button_labels:
            button = QPushButton(label)
            button.setFixedSize(300, 260)  # Taille des boutons (120px x 80px pour être plus large)
            button.setIcon(QIcon("assets/icons/add.png"))  # Ajouter une icône (mettre votre chemin ici)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #121F91;
                    border-radius: 8px;
                    color: #FFFFFF;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #F02B3D;
                }
                """
            )
            button.clicked.connect(button_actions[label])  # Connecter chaque bouton à son action
            action_layout.addWidget(button)

        # Ajouter la section action_layout en bas avec un stretch factor de 4 (80% de l'espace)
        grid_layout.addLayout(action_layout)
        grid_layout.setStretch(0, 1)  # 20% pour user_info_widget
        grid_layout.setStretch(1, 4)  # 80% pour action_layout
        
        # Ajouter la sidebar et les boutons au layout du contenu
        content_layout.addWidget(sidebar_container)  # Ajouter la sidebar à gauche
        content_layout.addLayout(grid_layout)  # Ajouter les boutons à droite

        # Ajouter le contenu principal (sidebar + boutons) au layout principal
        main_layout.addLayout(content_layout)

    def deconnexion(self):
        """Déconnecter l'utilisateur et revenir à la page de connexion"""
        self.session_manager.clear_session()  # Effacer la session
        self.ouvrir_connexion()  # Rediriger vers la fenêtre de connexion

    def ouvrir_connexion(self):
        from views.basiques.connexion_window import ConnexionWindow  # Importer ConnexionWindow pour la redirection
        """Ouvrir la fenêtre de connexion"""
        self.hide()  # Cacher la fenêtre actuelle
        self.connexion_window_best = ConnexionWindow()  # Passer l'instance courante en tant que parent à connexion_window
        self.connexion_window_best.show()
        
    def ouvrir_liste_pays(self):
        """Action pour ouvrir la fenêtre de pays Installer"""
        pays_installer = PaysInstallerWindow()
        pays_installer.exec_()  # Afficher la fenêtre en mode modal

    def ouvrir_organisation(self):
        """Action pour ouvrir la fenêtre d'information de l'organisation"""
        ouvrir_organisation = OrganisationWindow()
        ouvrir_organisation.exec_()  # Afficher la fenêtre en mode modal