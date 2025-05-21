from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QLabel, QLineEdit, QHBoxLayout)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray
import sys
import json

# Configuration - MUST UPDATE THESE
API_KEY = "sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN"
ENTRY_TEMPLATE_ID = "EXP25000021"
BASE_URL = f"https://faircraft.benchling.com/api/v2/entry-templates/{ENTRY_TEMPLATE_ID}"  # Using faircraft domain

from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                               QLabel, QLineEdit, QHBoxLayout)
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray
import sys
import json

# Configuration - MUST UPDATE THESE
API_KEY = "sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN"
ENTRY_TEMPLATE_ID = "tmpl_tv7m7B78"
BASE_URL = f"https://faircraft.benchling.com/api/v2/entry-templates/{ENTRY_TEMPLATE_ID}"  # Using faircraft domain


class BenchlingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benchling Notebook Template Updater")
        self.resize(600, 450)

        # Main layout
        main_layout = QVBoxLayout()

        # Test section
        test_group = QHBoxLayout()
        self.test_button = QPushButton("Test Connection")
        self.test_result = QLabel("Status: Not tested")
        test_group.addWidget(self.test_button)
        test_group.addWidget(self.test_result)

        # Update section
        update_group = QVBoxLayout()

        # Add your field inputs here...
        self.field1_input = QLineEdit()
        self.field2_input = QLineEdit()
        self.field3_input = QLineEdit()
        self.name_input = QLineEdit()

        self.update_button = QPushButton("Update Template")
        self.update_result = QLabel("Ready to update")

        # Add widgets to layout...

        # Update section
        update_group = QVBoxLayout()
        self.field1_label = QLabel("Field 1 Value:")
        self.field1_input = QLineEdit()
        self.field2_label = QLabel("Field 2 Value:")
        self.field2_input = QLineEdit()
        self.field3_label = QLabel("Field 3 Value:")
        self.field3_input = QLineEdit()
        self.name_label = QLabel("Entry Name:")
        self.name_input = QLineEdit()
        self.update_button = QPushButton("Update Template")
        self.update_result = QLabel("Enter values and click to update template")

        # Add widgets to update group
        update_group.addWidget(self.field1_label)
        update_group.addWidget(self.field1_input)
        update_group.addWidget(self.field2_label)
        update_group.addWidget(self.field2_input)
        update_group.addWidget(self.field3_label)
        update_group.addWidget(self.field3_input)
        update_group.addWidget(self.name_label)
        update_group.addWidget(self.name_input)
        update_group.addWidget(self.update_button)
        update_group.addWidget(self.update_result)

        # Add groups to main layout
        main_layout.addLayout(test_group)
        main_layout.addLayout(update_group)
        self.setLayout(main_layout)

        # Network manager
        self.manager = QNetworkAccessManager(self)
        self.test_button.clicked.connect(self.test_connection)
        self.update_button.clicked.connect(self.update_template)

    def test_connection(self):
        """Test if we can connect to the API"""
        self.test_result.setText("Testing connection...")
        QApplication.processEvents()  # Update UI immediately

        test_url = "https://faircraft.benchling.com/api/v2/users/me"  # Using faircraft domain

        request = QNetworkRequest(QUrl(test_url))

        # Set required headers
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"Authorization", f"Bearer {API_KEY}".encode('utf-8'))
        request.setRawHeader(b"Origin", b"https://faircraft.benchling.com")
        request.setRawHeader(b"Referer", b"https://faircraft.benchling.com/")

        reply = self.manager.get(request)
        reply.finished.connect(lambda: self.handle_test_response(reply))

    def handle_test_response(self, reply: QNetworkReply):
        """Handle the test response with detailed error reporting"""
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        headers = {bytes(key).decode(): bytes(value).decode() for key, value in reply.rawHeaderPairs()}

        if reply.error() == QNetworkReply.NetworkError.NoError:
            response_data = reply.readAll().data().decode()
            try:
                user_info = json.loads(response_data)
                msg = f"✅ Connected as {user_info.get('name', 'Unknown')}"
                self.test_result.setText(msg)
                print("Connection successful! User info:", user_info)
            except json.JSONDecodeError:
                msg = "⚠️ Connected but received unexpected response"
                self.test_result.setText(msg)
                print("Raw response:", response_data)
        else:
            error_msg = reply.errorString()
            error_data = reply.readAll().data().decode()

            # Build detailed error message
            detailed_msg = [
                f"❌ Connection failed (Status: {status_code})",
                f"Error: {error_msg}"
            ]

            if error_data:
                try:
                    error_json = json.loads(error_data)
                    detailed_msg.append(f"API Message: {error_json.get('error', {}).get('message')}")
                except:
                    detailed_msg.append(f"Raw response: {error_data}")

            detailed_msg.append(f"\nHeaders: {json.dumps(headers, indent=2)}")
            self.test_result.setText("\n".join(detailed_msg))
            print("Full error details:", "\n".join(detailed_msg))

        reply.deleteLater()

    def update_template(self):
        """Modified update function with proper headers"""
        # [Previous field value collection code...]

        # Prepare request with all required headers
        request = QNetworkRequest(QUrl(BASE_URL))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"Authorization", f"Bearer {API_KEY}".encode('utf-8'))
        request.setRawHeader(b"Origin", b"https://faircraft.benchling.com")
        request.setRawHeader(b"Referer", b"https://faircraft.benchling.com/")
        request.setRawHeader(b"Accept", b"application/json")

        # [Rest of your update logic...]

        reply = self.manager.sendCustomRequest(request, QByteArray(b"PATCH"), QByteArray(json_data))
        reply.finished.connect(lambda: self.handle_response(reply))

    def handle_response(self, reply: QNetworkReply):
        """Enhanced response handler"""
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        headers = {bytes(key).decode(): bytes(value).decode() for key, value in reply.rawHeaderPairs()}

        if reply.error() == QNetworkReply.NetworkError.NoError:
            # [Success handling code...]
            pass
        else:
            # [Enhanced error handling code...]
            pass


if __name__ == "__main__":

    """
    app = QApplication(sys.argv)
    window = BenchlingApp()
    window.show()
    sys.exit(app.exec())
    """
    print(f"Bearer {API_KEY}".encode('utf-8'))