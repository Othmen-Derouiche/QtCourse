import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)
print("Python console is working")  # Verify this appears

def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.addImportPath(sys.path[0])
    print(sys.path[0])
    engine.loadFromModule("App", "main")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()