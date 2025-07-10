from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QHeaderView
)
from PyQt5.QtCore import Qt
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager
from ui.edit_product_window import EditProductWindow


class ViewProductsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Products")
        self.resize(900, 500)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("📦 Products in Inventory")
        layout.addWidget(title_label)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Make headers resizable properly
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.load_products)
        layout.addWidget(refresh_btn)

        self.setLayout(layout)

        # Load products at start
        self.load_products()

    def load_products(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, c.name as category, p.sku, p.price, p.quantity_in_stock
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
        """)
        products = cursor.fetchall()
        conn.close()

        # Define headers
        headers = ["ID", "Name", "Category", "SKU", "Price", "Quantity", "Actions"]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(products))

        # Stretch last column for actions
        header = self.table.horizontalHeader()
        for col in range(len(headers) - 1):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(len(headers) - 1, QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        for row_idx, row_data in enumerate(products):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

            # Add Edit & Delete buttons
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)  # margin
            btn_layout.setSpacing(5)

            edit_btn = QPushButton("✏️ Edit")
            delete_btn = QPushButton("🗑️ Delete")

            # Set fixed size
            edit_btn.setFixedSize(100, 30)
            delete_btn.setFixedSize(100, 30)

            edit_btn.clicked.connect(lambda _, pid=row_data[0]: self.edit_product(pid))
            delete_btn.clicked.connect(lambda _, pid=row_data[0]: self.delete_product(pid))

            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)

            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)

            self.table.setCellWidget(row_idx, len(headers) - 1, btn_widget)

            # Ensure row is tall enough
            self.table.setRowHeight(row_idx, 40)

    def delete_product(self, product_id):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this product?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            conn = db_manager.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Deleted", "Product deleted successfully.")
            self.load_products()

    def edit_product(self, product_id):
        self.edit_window = EditProductWindow(product_id, self)
        self.edit_window.show()
