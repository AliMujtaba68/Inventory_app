from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLineEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager


class ManageUsersWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manage Users")
        self.resize(600, 400)

        layout = QVBoxLayout()

        # Title
        layout.addWidget(QLabel("👥 Manage Users"))

        # Add user controls
        form_layout = QHBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.role_dropdown = QComboBox()
        self.role_dropdown.addItems(['user', 'admin'])

        add_btn = QPushButton("➕ Add User")
        add_btn.clicked.connect(self.add_user)

        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.role_dropdown)
        form_layout.addWidget(add_btn)

        layout.addLayout(form_layout)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_users()

    def load_users(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(users))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Actions"])

        for row_idx, (uid, uname, role) in enumerate(users):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(uid)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(uname))
            self.table.setItem(row_idx, 2, QTableWidgetItem(role))

            # Delete button
            btn_layout = QHBoxLayout()
            del_btn = QPushButton("🗑️ Delete")
            del_btn.setFixedSize(80, 30)
            del_btn.clicked.connect(lambda _, user_id=uid: self.delete_user(user_id))
            btn_layout.addWidget(del_btn)

            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)
            self.table.setCellWidget(row_idx, 3, btn_widget)

    def add_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_dropdown.currentText()

        if not username or not password:
            QMessageBox.warning(self, "Validation Error", "Username and password are required.")
            return

        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password, role) VALUES (?, ?, ?)
            """, (username, password, role))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", f"User '{username}' added.")
            self.username_input.clear()
            self.password_input.clear()
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add user:\n{e}")

    def delete_user(self, user_id):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Deleted", "User deleted.")
            self.load_users()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete user:\n{e}")
