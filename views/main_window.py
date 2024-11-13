from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class MainWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.setWindowTitle("Application avec API")

        layout = QVBoxLayout()
        
        # Affiche l'URL de l'API pour vérifier la connexion
        layout.addWidget(QLabel(f"Connecté à l'API : {config['api_url']}"))
        
        # Logique d'appel de l'API peut être ajoutée ici
        self.setLayout(layout) 