from PySide6.QtGui import QIcon

class ImagePath:
    # Chemin de l'icône de l'application
    ICON_PATH = "assets/images/logoMemgesth.png"
    
    # Titre de la fenêtre
    TITLE = "Memgesth"

    @staticmethod
    def get_icon():
        """Retourne l'icône de l'application."""
        return QIcon(ImagePath.ICON_PATH)

    @staticmethod
    def get_title():
        """Retourne le titre de l'application."""
        return ImagePath.TITLE
