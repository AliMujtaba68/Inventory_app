from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QHeaderView, QLineEdit, QComboBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import os
import sys
import csv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager
from ui.edit_product_window import EditProductWindow


class ViewProductsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Products")
        self.resize(1000, 600)

        layout = QVBoxLayout()

        # Title
        title_label = QLabel("📦 Products in Inventory")
        layout.addWidget(title_label)

        # Filters
        filter_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search by Name or SKU")
        self.search_input.textChanged.connect(self.load_products)

        self.category_dropdown = QComboBox()
        self.category_dropdown.addItem("All Categories", None)
        self.category_dropdown.currentIndexChanged.connect(self.load_products)

        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(self.category_dropdown)

        layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Make headers resizable properly
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)

        # Buttons below table
        btns_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 Reset Filters")
        refresh_btn.clicked.connect(self.reset_filters)

        export_btn = QPushButton("📄 Export to CSV")
        export_btn.clicked.connect(self.export_to_csv)

        btns_layout.addWidget(refresh_btn)
        btns_layout.addWidget(export_btn)
        btns_layout.addStretch()
        layout.addLayout(btns_layout)

        self.setLayout(layout)

        # Load categories & products at start
        self.load_categories()
        self.load_products()

    def load_categories(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        for cat_id, cat_name in categories:
            self.category_dropdown.addItem(cat_name, cat_id)

    def load_products(self):
        self.products_data = []

        search_text = self.search_input.text().strip()
        selected_category = self.category_dropdown.currentData()

        conn = db_manager.get_connection()
        cursor = conn.cursor()

        query = """
            SELECT p.id, p.name, c.name as category, p.sku, p.price, p.quantity_in_stock
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE 1=1
        """
        params = []

        if search_text:
            query += " AND (p.name LIKE ? OR p.sku LIKE ?)"
            params.extend([f"%{search_text}%", f"%{search_text}%"])

        if selected_category:
            query += " AND p.category_id = ?"
            params.append(selected_category)

        cursor.execute(query, params)
        products = cursor.fetchall()
        conn.close()

        self.products_data = products

        headers = ["ID", "Name", "Category", "SKU", "Price", "Quantity", "Actions"]

        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(products))

        header = self.table.horizontalHeader()
        for col in range(len(headers) - 1):
            header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(len(headers) - 1, QHeaderView.Stretch)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

        low_stock_found = False

        for row_idx, row_data in enumerate(products):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)

                # Highlight low stock
                if col_idx == 5 and int(cell_data) < 5:
                    item.setBackground(QColor(255, 200, 200))
                    low_stock_found = True

                self.table.setItem(row_idx, col_idx, item)

            # Add Edit & Delete buttons
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(2, 2, 2, 2)
            btn_layout.setSpacing(5)

            edit_btn = QPushButton("✏️ Edit")
            delete_btn = QPushButton("🗑️ Delete")

            edit_btn.setFixedSize(100, 30)
            delete_btn.setFixedSize(100, 30)

            edit_btn.clicked.connect(lambda _, pid=row_data[0]: self.edit_product(pid))
            delete_btn.clicked.connect(lambda _, pid=row_data[0]: self.delete_product(pid))

            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)

            btn_widget = QWidget()
            btn_widget.setLayout(btn_layout)

            self.table.setCellWidget(row_idx, len(headers) - 1, btn_widget)

            self.table.setRowHeight(row_idx, 40)

        if low_stock_found:
            QMessageBox.warning(self, "⚠️ Low Stock", "Some products have low stock (<5)!")

    def reset_filters(self):
        self.search_input.clear()
        self.category_dropdown.setCurrentIndex(0)
        self.load_products()

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

            cursor.execute("SELECT name FROM products WHERE id=?", (product_id,))
            result = cursor.fetchone()
            product_name = result[0] if result else "Unknown"

            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            conn.close()

            db_manager.log_action("admin", "Deleted", product_name)

            QMessageBox.information(self, "Deleted", f"Product '{product_name}' deleted successfully.")
            self.load_products()

    def edit_product(self, product_id):
        self.edit_window = EditProductWindow(product_id, self)
        self.edit_window.show()

    def export_to_csv(self):
        if not self.products_data:
            QMessageBox.warning(self, "No Data", "There is no data to export.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save File", "products_export.csv", "CSV Files (*.csv)")
        if not path:
            return

        try:
            with open(path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Category", "SKU", "Price", "Quantity"])
                for row in self.products_data:
                    writer.writerow(row)

            QMessageBox.information(self, "Exported", f"Data exported to:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export:\n{e}")
