import sys

from PySide6.QtCore import Slot
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QStatusBar, QCalendarWidget, QLCDNumber, QLabel, \
    QPushButton, QLineEdit, QCheckBox, QSpinBox, QSlider, QProgressBar


# On définit une classe de fenêtre par héritage.
class MyWindow(QMainWindow):

    # Le constructeur de la classe nous permet de changer quelques caractéristiques.
    def __init__(self):
        # Appel au constructeur parent (QMainWindow).
        super().__init__()
        # On change le titre de la fenêtre.
        self.setWindowTitle("Ma première fenêtre Qt avec Python")
        # On change l'icône affichée dans le bandeau supérieur de la fenêtre.
        self.setWindowIcon(QIcon("icons/_active__cut.png"))
        # On retaille la fenêtre (800 pixels de large et 600 en hauteur).
        self.resize(800, 600)

        self.setMaximumSize(1200,1000)
        self.setMinimumSize(1000,800)
        self.setToolTip("Fuck Me")

        # Le type QWidget représente un conteneur de widgets (et il est lui-même un widget).
        # On crée une instance que l'on va mettre au centre de la fenêtre.
        centralArea = QWidget()
        # On lui met une couleur d'arrière-plan, histoire de bien le voir.
        #centralArea.setStyleSheet("background: #d7ebea")
        centralArea.setObjectName("centralArea")
        # On injecte ce widget en tant que zone centrale.
        self.setCentralWidget(centralArea)


        statusBar = self.statusBar()  #QStatusBar(self) # what is the difference ?
        statusBar.setStyleSheet("background: #bac4c4 ")
        statusBar.showMessage("this is my status bar ")

        menuBar = self.menuBar()
        menuBar.setStyleSheet("background: #73e3de")
        fileMenu = menuBar.addMenu("File")
        fileMenu.addSeparator()

        # On place maintenant chacun des composants souhaités dans la zone centrale.
        calendar = QCalendarWidget(centralArea)
        calendar.setGeometry(10, 10, 300, 200)
        # On connecte le signal selectionChanged exposé par le calendier au slot dateSelected.
        calendar.selectionChanged.connect(self.dateSelected)

        lcd = QLCDNumber(self)
        lcd.display(1234)
        lcd.setGeometry(10, 220, 300, 70)

        label = QLabel("A label with <b style='color: red'>HTML</b> text" , centralArea)
        label.setGeometry(320, 10, 270, 30)

        # On définit ici notre lien (un QLabel avec un tag HTML de lien).
        labelHelp = QLabel("<a href='https://koor.fr'>Obtenir l'aide en ligne</a>", centralArea)
        labelHelp.setStyleSheet("font-size: 20px;")
        labelHelp.setGeometry(20, 100, 200, 30)

        button = QPushButton("This is a button", centralArea)
        button.setGeometry(320, 50, 270, 30)
        button.setToolTip("""<b>Qt</b> is <u>very</u> <i>Good</i> 
                              <hr/>
                              <ul>
                                  <li>First item</li>
                                  <li>Second item</li>
                                  <li style='color:red'>Last item</li>
                              </ul>
                              <br/> 
                              <img src="QtCourse/icons/zoom_in.png" />
                              """)
        # On connecte le signal clicked exposé par le bouton au slot dateSelected.
        button.clicked.connect(self.buttonClicked)

        textBox = QLineEdit("This is a text box", centralArea)
        textBox.setGeometry(320, 90, 270, 30)

        checkBox = QCheckBox("This is a check box", centralArea)
        checkBox.setGeometry(320, 130, 270, 30)

        spinBox = QSpinBox(centralArea)
        spinBox.setValue(50)
        spinBox.setGeometry(320, 170, 270, 30)

        slider = QSlider(Qt.Horizontal, centralArea)
        slider.setValue(50)
        slider.setGeometry(320, 220, 270, 30)
        # On connecte le signal valueChanged exposé par le slider au slot valueChanged.
        slider.valueChanged.connect(self.valueChanged)

        progress = QProgressBar(centralArea)
        progress.setValue(50)
        progress.setGeometry(320, 260, 270, 30)

        btnOk = QPushButton("Ok", centralArea)
        #btnOk.setStyleSheet("background: green; color: white; font-size: bold;")
        btnOk.setGeometry(360, 500, 100, 60)
        btnOk.setObjectName("btnOk")

        btnCancel = QPushButton("Cancel", centralArea)
        btnCancel.setStyleSheet("background: red; color: green;") # code qss embarqué dans le code python
        btnCancel.setGeometry(480, 500, 100, 40)

    @Slot()
    def dateSelected(self):
        calendar: QCalendarWidget = self.sender()
        print(f"Selected date is {calendar.selectedDate()}")

    @Slot()
    def buttonClicked(self):
        btn : QPushButton = self.sender()
        print(f"Button <{btn.text()}> clicked")
        btn.setText("Back to main menu")
    @Slot(int)
    def valueChanged(self, value: int):
        slider = self.sender()
        print(f"Slider selected value is { value }-{slider.value()}")


if __name__ == "__main__":
    # On crée l'instance d'application en lui passant le tableau des arguments.
    app = QApplication(sys.argv)

    # On instancie une fenêtre graphique et l'affiche.
    myWindow = MyWindow()
    myWindow.show()

    # On démarre la boucle de gestion des événements.
    sys.exit(app.exec())