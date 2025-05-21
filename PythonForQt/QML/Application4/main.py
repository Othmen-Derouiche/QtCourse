import os
import sys
import json
from datetime import datetime
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine


class DefectDetector(QObject):
    def __init__(self):
        super().__init__()
        self._image_path = ""
        self._defects = []
        self._processing_time = 0
        self._model_version = "2.1.3"
        self._confidence_threshold = 75
        self._iou_threshold = 0.5
        self._detection_mode = "Standard"
        self._active_classes = {
            "Solder Defect": True,
            "Component Misalignment": True,
            "Trace Break": True,
            "Missing Component": True
        }
        self._status_message = "Ready"

    # Signals
    imageChanged = Signal()
    defectsChanged = Signal()
    statusChanged = Signal()
    processingComplete = Signal()

    # Properties
    @Property(str, notify=imageChanged)
    def imagePath(self):
        return self._image_path

    @Property(list, notify=defectsChanged)
    def defects(self):
        return self._defects

    @Property(float, notify=defectsChanged)
    def processingTime(self):
        return self._processing_time

    @Property(str, notify=defectsChanged)
    def modelVersion(self):
        return self._model_version

    @Property(int, notify=defectsChanged)
    def confidenceThreshold(self):
        return self._confidence_threshold

    @Property(float, notify=defectsChanged)
    def iouThreshold(self):
        return self._iou_threshold

    @Property(str, notify=defectsChanged)
    def detectionMode(self):
        return self._detection_mode

    @Property(str, notify=statusChanged)
    def statusMessage(self):
        return self._status_message

    # Slots
    @Slot(str)
    def loadImage(self, path):
        if os.path.exists(path):
            self._image_path = path
            self._status_message = f"Loaded: {os.path.basename(path)}"
            self.imageChanged.emit()
            self.statusChanged.emit()

    @Slot()
    def runDetection(self):
        self._status_message = "Processing image..."
        self.statusChanged.emit()

        # Simulate processing delay
        QTimer.singleShot(1200, self._completeDetection)

    def _completeDetection(self):
        # Simulated defect data - in a real app this would come from your detection model
        self._defects = [
            {
                "id": 1,
                "type": "Solder Defect",
                "x": 750,
                "y": 300,
                "width": 40,
                "height": 40,
                "confidence": 98.7,
                "severity": "Critical",
                "action": "Reject"
            },
            {
                "id": 2,
                "type": "Component Misalignment",
                "x": 420,
                "y": 170,
                "width": 30,
                "height": 20,
                "confidence": 87.5,
                "severity": "Medium",
                "action": "Review"
            },
            {
                "id": 3,
                "type": "Trace Break",
                "x": 540,
                "y": 420,
                "width": 15,
                "height": 5,
                "confidence": 92.3,
                "severity": "Low",
                "action": "Monitor"
            }
        ]

        self._processing_time = 1.2
        self._status_message = "Detection complete"
        self.defectsChanged.emit()
        self.statusChanged.emit()
        self.processingComplete.emit()

    @Slot(int)
    def setConfidenceThreshold(self, value):
        self._confidence_threshold = value
        self.defectsChanged.emit()

    @Slot(float)
    def setIouThreshold(self, value):
        self._iou_threshold = value
        self.defectsChanged.emit()

    @Slot(str)
    def setDetectionMode(self, mode):
        self._detection_mode = mode
        self.defectsChanged.emit()

    @Slot(str, bool)
    def toggleDefectClass(self, class_name, active):
        self._active_classes[class_name] = active
        self.defectsChanged.emit()

    @Slot(int)
    def getDefectDetails(self, defect_id):
        for defect in self._defects:
            if defect["id"] == defect_id:
                return json.dumps(defect)
        return "{}"


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the detector instance
    detector = DefectDetector()

    # Set up QML engine
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("detector", detector)

    # Load the QML file
    engine.load("Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())