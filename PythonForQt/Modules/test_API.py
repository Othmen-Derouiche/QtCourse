from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray

import sys
import json


API_KEY = "YOUR_BENCHLING_API_KEY"
SCHEMA_ID = "EXP25000021"
BASE_URL = "https://YOUR_TENANT.benchling.com/api/v2/custom-entities"  # Example endpoint

class BenchlingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benchling API Test")
        self.resize(400, 150)

        layout = QVBoxLayout()
        self.status_label = QLabel("Click to send data to Benchling")
        self.send_button = QPushButton("Send Test Data")

        layout.addWidget(self.status_label)
        layout.addWidget(self.send_button)
        self.setLayout(layout)

        self.manager = QNetworkAccessManager(self)
        self.send_button.clicked.connect(self.send_data)

    def send_data(self):
        # Use Python dict to represent JSON data
        payload = {
            "name": "Test Sample",
            "schemaId": SCHEMA_ID,
            "fields": {
                "testField": "Hello Benchling"
            }
        }

        # Convert Python dict to JSON string and then to QByteArray
        json_data = json.dumps(payload).encode('utf-8')

        # Create and configure the request
        request = QNetworkRequest(QUrl(BASE_URL))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"Authorization", f"Bearer {API_KEY}".encode('utf-8'))

        # Send the request
        reply = self.manager.post(request, QByteArray(json_data))
        reply.finished.connect(lambda: self.handle_response(reply))

    def handle_response(self, reply: QNetworkReply):
        if reply.error() == QNetworkReply.NetworkError.NoError:
            response_data = reply.readAll().data().decode()
            self.status_label.setText("✅ Data sent successfully!")
            print("Response:", response_data)
        else:
            error_msg = reply.errorString()
            self.status_label.setText(f"❌ Error: {error_msg}")
            print("Error:", error_msg)
        reply.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BenchlingApp()
    window.show()
    sys.exit(app.exec())