from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Dashboard")

        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome to the Dashboard, {username}!")
        layout.addWidget(welcome_label)

        self.setLayout(layout)
