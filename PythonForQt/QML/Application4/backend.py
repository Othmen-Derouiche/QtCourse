from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide6.QtGui import QImage, QPixmap
import os

class DefectDetector(QObject):
    def __init__(self):
        super().__init__()
        self._image_path = ""
        self._defects = []
        self._status_message = "Ready"
        self._processing_time = 0.0
        self._confidence_threshold = 75
        self._iou_threshold = 0.5
        self._detection_mode = "Standard"
        self._model_version = "2.1.3"

    # Signals
    imageLoaded = Signal()
    defectsUpdated = Signal()
    statusChanged = Signal(str)
    confidenceThresholdChanged = Signal()
    iouThresholdChanged = Signal()
    detectionModeChanged = Signal()

    # Properties
    @Property(str, notify=imageLoaded)
    def imagePath(self):
        return self._image_path

    @Property(list, notify=defectsUpdated)
    def defects(self):
        return self._defects

    @Property(str, notify=statusChanged)
    def statusMessage(self):
        return self._status_message

    @Property(float, notify=statusChanged)
    def processingTime(self):
        return self._processing_time

    @Property(int, notify=confidenceThresholdChanged)
    def confidenceThreshold(self):
        return self._confidence_threshold

    @Property(float, notify=iouThresholdChanged)
    def iouThreshold(self):
        return self._iou_threshold

    @Property(str, notify=detectionModeChanged)
    def detectionMode(self):
        return self._detection_mode

    @Property(str, constant=True)
    def modelVersion(self):
        return self._model_version

    # Slots
    @Slot(str)
    def loadImage(self, file_path):
        if os.path.exists(file_path):
            self._image_path = file_path
            self._status_message = f"Loaded: {os.path.basename(file_path)}"
            self.imageLoaded.emit()
            self.statusChanged.emit(self._status_message)

    @Slot()
    def runDetection(self):
        self._status_message = "Running detection..."
        self.statusChanged.emit(self._status_message)
        
        # Simulate detection
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
            }
        ]
        
        self._processing_time = 1.2
        self._status_message = "Detection complete"
        self.defectsUpdated.emit()
        self.statusChanged.emit(self._status_message)

    @Slot(int)
    def setConfidenceThreshold(self, value):
        self._confidence_threshold = value
        self.confidenceThresholdChanged.emit()

    @Slot(float)
    def setIouThreshold(self, value):
        self._iou_threshold = value
        self.iouThresholdChanged.emit()

    @Slot(str)
    def setDetectionMode(self, mode):
        self._detection_mode = mode
        self.detectionModeChanged.emit()

    @Slot(str, bool)
    def toggleDefectClass(self, defect_class, enabled):
        print(f"Toggled {defect_class} to {enabled}")