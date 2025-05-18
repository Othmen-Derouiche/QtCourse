import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.engine().addImportPath(sys.path[0]) # Add the current directory to the import paths and load the main module.
    view.loadFromModule("App", "Main") #  load a QML file structured as a module :  look for a qmldir file in the App folder that defines the Main QML type
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.show()
    ex = app.exec()
    del view
    sys.exit(ex)