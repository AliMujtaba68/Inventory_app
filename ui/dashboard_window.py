from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
)

from ui.view_products_window import ViewProductsWindow
from ui.add_product_window import AddProductWindow
from ui.view_logs_window import ViewLogsWindow
from ui.manage_users_window import ManageUsersWindow  # 👥 new import

from models.backup_restore import backup_database, restore_database  # 💾 new import


class DashboardWindow(QWidget):
    def __init__(self, username, role='user'):
        super().__init__()
        self.username = username
        self.role = role

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
        self.manage_users_btn = QPushButton("👥 Manage Users")  # 👥 new button
        self.backup_btn = QPushButton("💾 Backup Database")      # 💾 new button
        self.restore_btn = QPushButton("♻️ Restore Database")   # ♻️ new button
        self.logout_btn = QPushButton("🚪 Logout")

        # Connect buttons to handlers
        self.view_products_btn.clicked.connect(self.view_products)
        self.add_product_btn.clicked.connect(self.add_product)
        self.view_logs_btn.clicked.connect(self.view_logs)
        self.manage_users_btn.clicked.connect(self.manage_users)  # 👥 connect
        self.backup_btn.clicked.connect(self.backup_db)           # 💾 connect
        self.restore_btn.clicked.connect(self.restore_db)         # ♻️ connect
        self.logout_btn.clicked.connect(self.logout)

        # Add buttons to layout
        layout.addWidget(self.view_products_btn)
        layout.addWidget(self.add_product_btn)
        layout.addWidget(self.view_logs_btn)

        # 👥 only show Manage Users if admin
        if self.role == 'admin':
            layout.addWidget(self.manage_users_btn)

        # 💾 backup & restore available to admin only
        if self.role == 'admin':
            layout.addWidget(self.backup_btn)
            layout.addWidget(self.restore_btn)

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

    def manage_users(self):
        self.users_window = ManageUsersWindow()
        self.users_window.show()

    def backup_db(self):
        backup_database(self)

    def restore_db(self):
        restore_database(self)

    def logout(self):
        QMessageBox.information(self, "Logout", "Logging out…")
        self.close()
