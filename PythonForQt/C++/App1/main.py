import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow


# On définit une classe de fenêtre par héritage.
class MyWindow(QMainWindow):

    # Le constructeur de la classe nous permet de changer quelques caractéristiques.
    def __init__(self):
        # Appel au constructeur parent (QMainWindow).
        super().__init__()
        # On change le titre de la fenêtre.
        self.setWindowTitle("Ma première fenêtre Qt avec Python")
        # On change l'icône affichée dans le bandeau supérieur de la fenêtre.
        self.setWindowIcon(QIcon("icons/yes.png"))
        # On retaille la fenêtre (800 pixels de large et 600 en hauteur).
        self.resize(800, 600)

        self.setMaximumSize(1200,1000)
        self.setToolTip("Fuck Me")


if __name__ == "__main__":
    # On crée l'instance d'application en lui passant le tableau des arguments.
    app = QApplication(sys.argv)

    # On instancie une fenêtre graphique et l'affiche.
    myWindow = MyWindow()
    myWindow.show()

    # On démarre la boucle de gestion des événements.
    sys.exit(app.exec())