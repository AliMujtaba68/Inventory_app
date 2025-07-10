from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
)

from ui.view_products_window import ViewProductsWindow
from ui.add_product_window import AddProductWindow
from ui.view_logs_window import ViewLogsWindow


class DashboardWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("Dashboard")

        # Main layout
        layout = QVBoxLayout()

        # Welcome message
        welcome_label = QLabel(f"Welcome to the Dashboard, {username}!")
        layout.addWidget(welcome_label)

        # Buttons
        self.view_products_btn = QPushButton("📦 View Products")
        self.add_product_btn = QPushButton("➕ Add Product")
        self.view_logs_btn = QPushButton("📊 View Inventory Logs")
        self.logout_btn = QPushButton("🚪 Logout")

        # Connect buttons to handlers
        self.view_products_btn.clicked.connect(self.view_products)
        self.add_product_btn.clicked.connect(self.add_product)
        self.view_logs_btn.clicked.connect(self.view_logs)
        self.logout_btn.clicked.connect(self.logout)

        # Add buttons to layout
        layout.addWidget(self.view_products_btn)
        layout.addWidget(self.add_product_btn)
        layout.addWidget(self.view_logs_btn)
        layout.addWidget(self.logout_btn)

        # Set layout
        self.setLayout(layout)

    def view_products(self):
        self.products_window = ViewProductsWindow()
        self.products_window.show()

    def add_product(self):
        self.add_product_window = AddProductWindow()
        self.add_product_window.show()

    def view_logs(self):
        self.logs_window = ViewLogsWindow()
        self.logs_window.show()

    def logout(self):
        QMessageBox.information(self, "Logout", "Logging out…")
        self.close()
