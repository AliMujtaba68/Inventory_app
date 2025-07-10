from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMessageBox
)
from PyQt5.QtCore import Qt
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager


class ViewLogsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📜 Inventory Logs")
        self.resize(800, 500)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("📜 Action Logs")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Refresh Button
        refresh_btn = QPushButton("🔄 Refresh Logs")
        refresh_btn.clicked.connect(self.load_logs)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)

        self.load_logs()

    def load_logs(self):
        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT timestamp, username, action, product_name
                FROM logs
                ORDER BY timestamp DESC
            """)
            logs = cursor.fetchall()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load logs:\n{e}")
            return

        headers = ["Timestamp", "User", "Action", "Product Name"]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(logs))

        header = self.table.horizontalHeader()
        for col in range(len(headers)):
            header.setSectionResizeMode(col, QHeaderView.Stretch)

        if not logs:
            QMessageBox.information(self, "Logs", "No logs found.")
            return

        for row_idx, row_data in enumerate(logs):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)
