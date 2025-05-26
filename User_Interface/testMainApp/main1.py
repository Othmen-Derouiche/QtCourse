import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from backend import DefectDetector

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    # Create detector instance
    detector = DefectDetector()
    
    engine = QQmlApplicationEngine()
    
    # Expose Python object to QML
    engine.rootContext().setContextProperty("detector", detector)
    
    # Add the current directory to the import paths and load the main module.
    engine.addImportPath(sys.path[0])
    engine.loadFromModule("App", "Main")
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec())