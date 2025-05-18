import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel , QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
)
from PySide6.QtGui import QPixmap, QWheelEvent , QImage
from PySide6.QtCore import Qt

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self._zoom = 0

    def wheelEvent(self, event: QWheelEvent):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
            self._zoom += 1
        else:
            zoom_factor = zoom_out_factor
            self._zoom -= 1

        if self._zoom < -10:
            self._zoom = -10
            return
        elif self._zoom > 20:
            self._zoom = 20
            return

        self.scale(zoom_factor, zoom_factor)


class ImageViewer(QMainWindow):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("Zoomable Image Viewer")

        # Load image
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            raise ValueError(f"Cannot load image from: {image_path}")

        # Create scene and view
        self.scene = QGraphicsScene(self)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.pixmap_item)

        self.view = ZoomableGraphicsView(self)
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

if __name__ == "__main__":
    image_path = "C:/Users/othme/Desktop/R10B1S3MP2.png"

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File does not exist: {image_path}")


    app = QApplication(sys.argv)
    window = ImageViewer(image_path)
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
