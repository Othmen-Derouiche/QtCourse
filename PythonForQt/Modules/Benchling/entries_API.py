import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QTextEdit, QLabel, QLineEdit)
from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

API_KEY = "sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN"
class BenchlingApiClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benchling API Client")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # API URL input
        self.url_label = QLabel("API URL:")
        self.url_input = QLineEdit("https://faircraft.benchling.com/api/v2/entries?pageSize=3&sort=modifiedAt%3Adesc&name=test_API") # request URL
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Authorization token input
        self.token_label = QLabel("API KEY:")
        self.token_input = QLineEdit(API_KEY)
        self.token_input.setPlaceholderText("Hello")
        self.token_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.token_label)
        layout.addWidget(self.token_input)

        # Button to send request
        self.send_button = QPushButton("Send GET Request")
        self.send_button.clicked.connect(self.send_request)
        layout.addWidget(self.send_button)

        # Response display
        self.response_label = QLabel("Response:")
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        layout.addWidget(self.response_label)
        layout.addWidget(self.response_output)

        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        # Network manager
        self.network_manager = QNetworkAccessManager(self)

        # Set default token (optional - remove in production)
        self.token_input.setText(API_KEY)

    def send_request(self):
        url = self.url_input.text().strip()
        token = self.token_input.text().strip()
        print(url)
        print(f"Bearer {token}".encode())

        if not url:
            self.status_label.setText("Error: URL is required")
            return

        if not token:
            self.status_label.setText("Error: Authorization token is required")
            return

        # Create request
        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"accept", b"application/json")
        request.setRawHeader(b"Authorization", "f{API_KEY}".encode()) #f"Bearer {token}".encode()

        self.status_label.setText("Sending request...")
        self.response_output.clear()

        # Send GET request
        self.network_manager.get(request).finished.connect(self.handle_response)

    def handle_response(self):
        reply = self.sender()

        if reply.error() == QNetworkReply.NoError:
            # Read and format the response
            data = reply.readAll().data()
            try:
                json_data = json.loads(data)
                formatted_response = json.dumps(json_data, indent=2)
                self.response_output.setPlainText(formatted_response)
                self.status_label.setText("Request successful")
            except json.JSONDecodeError:
                self.response_output.setPlainText(data.decode())
                self.status_label.setText("Request successful (non-JSON response)")
        else:
            error_message = f"Error: {reply.errorString()}"
            self.response_output.setPlainText(error_message)
            self.status_label.setText("Request failed")

        reply.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BenchlingApiClient()
    window.show()
    sys.exit(app.exec())