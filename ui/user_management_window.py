from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QHeaderView, QMessageBox, QLineEdit,
    QComboBox, QDialog, QFormLayout, QDialogButtonBox
)
from PyQt5.QtCore import Qt
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager


class UserManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.resize(600, 400)

        layout = QVBoxLayout()
        title = QLabel("👤 User Management")
        layout.addWidget(title)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add User")
        add_btn.clicked.connect(self.add_user_dialog)
        btn_layout.addWidget(add_btn)

        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_users)
        btn_layout.addWidget(refresh_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        self.users = db_manager.get_all_users()
        headers = ["ID", "Username", "Role", "Actions"]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(self.users))

        header = self.table.horizontalHeader()
        for col in range(len(headers) - 1):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(len(headers) - 1, QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        for row_idx, user in enumerate(self.users):
            for col_idx, cell_data in enumerate(user):
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

            # Actions
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)

            edit_btn = QPushButton("✏️ Edit")
            delete_btn = QPushButton("🗑️ Delete")

            edit_btn.setFixedSize(80, 30)
            delete_btn.setFixedSize(80, 30)

            edit_btn.clicked.connect(lambda _, uid=user[0]: self.edit_user_dialog(uid))
            delete_btn.clicked.connect(lambda _, uid=user[0]: self.delete_user(uid))

            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)

            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)

            self.table.setCellWidget(row_idx, len(headers) - 1, btn_widget)

            self.table.setRowHeight(row_idx, 40)

    def add_user_dialog(self):
        dialog = UserDialog()
        if dialog.exec_() == QDialog.Accepted:
            username, password, role = dialog.get_data()
            try:
                db_manager.add_user(username, password, role)
                QMessageBox.information(self, "Success", "User added.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to add user:\n{e}")

    def edit_user_dialog(self, user_id):
        dialog = UserDialog(edit=True)
        if dialog.exec_() == QDialog.Accepted:
            password, role = dialog.get_data(edit=True)
            try:
                db_manager.update_user(user_id, password=password, role=role)
                QMessageBox.information(self, "Success", "User updated.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to update user:\n{e}")

    def delete_user(self, user_id):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                db_manager.delete_user(user_id)
                QMessageBox.information(self, "Deleted", "User deleted.")
                self.load_users()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user:\n{e}")


class UserDialog(QDialog):
    def __init__(self, edit=False):
        super().__init__()
        self.setWindowTitle("Edit User" if edit else "Add User")
        self.resize(300, 150)

        layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.role_dropdown = QComboBox()
        self.role_dropdown.addItems(["user", "admin"])

        if not edit:
            layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)
        layout.addRow("Role:", self.role_dropdown)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)

        layout.addRow(btn_box)
        self.setLayout(layout)

        self.edit = edit

    def get_data(self, edit=False):
        if not edit:
            return (
                self.username_input.text().strip(),
                self.password_input.text().strip(),
                self.role_dropdown.currentText()
            )
        else:
            return (
                self.password_input.text().strip(),
                self.role_dropdown.currentText()
            )


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = UserManagementWindow()
    win.show()
    sys.exit(app.exec_())
