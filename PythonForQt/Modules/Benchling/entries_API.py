from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtCore import QUrl
import sys
import base64

API_KEY = "sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN"

API_URL1 = "https://faircraft.benchling.com/api/v2/entries" #get list of entries
API_URL2 = "https://faircraft.benchling.com/api/v2/entries?pageSize=2&sort=createdAt" #get entries with filter 
API_URL3 = ""
API_URL4 = ""

projet_API_ID = ""
result_table_API_ID = "assaysch_sIyBpyet"

class APIClient(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Benchling API Client")

        # UI elements
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter API URL")

        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Enter API Key ")
        self.token_input.setEchoMode(QLineEdit.Password)

        self.send_button = QPushButton("Send Request")
        self.send_button.clicked.connect(self.send_request)

        self.status_label = QLabel("Ready")
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Benchling API URL:"))
        layout.addWidget(self.url_input)
        layout.addWidget(QLabel("API Key:"))
        layout.addWidget(self.token_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.status_label)
        layout.addWidget(QLabel("Response:"))
        layout.addWidget(self.response_output)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.network_manager = QNetworkAccessManager()

    def send_request(self):
        url = self.url_input.text().strip()
        api_key = self.token_input.text().strip()

        if not url:
            self.status_label.setText("Error: URL is required")
            return
        if not api_key:
            self.status_label.setText("Error: API Key is required")
            return

        # Encode API key as Basic Auth header (API_KEY + colon)
        credentials = f"{api_key}:".encode("utf-8")
        base64_credentials = base64.b64encode(credentials).decode("utf-8")

        request = QNetworkRequest(QUrl(url))
        request.setRawHeader(b"Accept", b"application/json")
        request.setRawHeader(b"Authorization", f"Basic {base64_credentials}".encode())

        self.status_label.setText("Sending request...")
        self.response_output.clear()

        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.handle_response(reply))

    def handle_response(self, reply):
        if reply.error():
            self.status_label.setText(f"Error: {reply.errorString()}")
            response_data = reply.readAll().data().decode()
        else:
            self.status_label.setText("Request successful")
            response_data = reply.readAll().data().decode()

        self.response_output.setPlainText(response_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = APIClient()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
