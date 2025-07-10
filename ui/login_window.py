import sys
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)

# Add the project root to sys.path so we can import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager
from ui.dashboard_window import DashboardWindow


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        layout = QVBoxLayout()

        # Username field
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password field
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Query the database
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            # Login successful → open dashboard
            self.dashboard = DashboardWindow(username)
            self.dashboard.show()
            self.close()
        else:
            # Login failed → show error
            QMessageBox.warning(self, "Error", "Invalid username or password.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
