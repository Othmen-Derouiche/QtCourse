from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QHBoxLayout
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtCore import QUrl, QByteArray

import sys
import json

"""
{
  "error": {
    "message": "Found an unexpected field: modifiedAt",
    "type": "invalid_request_error",
    "userMessage": "Found an unexpected field: modifiedAt"
  }
}
"""
#API_ID = "etr_BilEbrx9"
API_KEY = "sk_CpxpzLhTngcdQgCGC3dH0qkEYSGHN"
#SCHEMA_ID = "EXP25000021"
# This should be the specific entry template ID you want to update (not schema ID)
ENTRY_TEMPLATE_ID =  "EXP25000021" # "etr_BilEbrx9" #
BASE_URL = f"https://faircraft.benchling.com/api/v2/entry-templates/{ENTRY_TEMPLATE_ID}"


class BenchlingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benchling Notebook Template Updater")
        self.resize(500, 400)

        # Main layout
        main_layout = QVBoxLayout()

        # Test section
        test_group = QHBoxLayout()
        self.test_button = QPushButton("Test Authentication")
        self.test_result = QLabel("Click to test authentication")
        test_group.addWidget(self.test_button)
        test_group.addWidget(self.test_result)

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

        # Connect signals
        self.test_button.clicked.connect(self.test_authentication)
        self.update_button.clicked.connect(self.update_template)

    def test_authentication(self):
        """Test if we can authenticate with the API"""
        self.test_result.setText("Testing authentication...")

        test_url = "https://benchling.com/api/v2/users/me"  # Simple endpoint to test auth

        request = QNetworkRequest(QUrl(test_url))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        request.setRawHeader(b"Authorization", f"Bearer {API_KEY}".encode('utf-8'))

        reply = self.manager.get(request)
        reply.finished.connect(lambda: self.handle_test_response(reply))

    def handle_test_response(self, reply: QNetworkReply):
        """Handle the authentication test response"""
        if reply.error() == QNetworkReply.NetworkError.NoError:
            response_data = reply.readAll().data().decode()
            try:
                user_info = json.loads(response_data)
                self.test_result.setText(f"✅ Authenticated as {user_info.get('name', 'Unknown')}")
                print("Authentication successful! User info:", user_info)
            except json.JSONDecodeError:
                self.test_result.setText("✅ Authenticated (no user data)")
                print("Auth test response headers:", reply.rawHeaderPairs())
        else:
            error_msg = reply.errorString()
            error_data = reply.readAll().data().decode()

            detailed_msg = f"❌ Authentication failed: {error_msg}"
            if error_data:
                try:
                    error_json = json.loads(error_data)
                    detailed_msg += f"\n{error_json.get('error', {}).get('message', 'Unknown error')}"
                except:
                    detailed_msg += f"\nRaw response: {error_data}"

            self.test_result.setText(detailed_msg)
            print("Auth test error details:", error_data)

        reply.deleteLater()

    def update_template(self):
        """Original update template function (unchanged from previous example)"""
        # [Rest of your existing update_template function code]
        pass

    def handle_response(self, reply: QNetworkReply):
        """Original response handler (unchanged from previous example)"""
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BenchlingApp()
    window.show()
    sys.exit(app.exec())



