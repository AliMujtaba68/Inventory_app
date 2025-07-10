from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox
)
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager


class AddProductWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        self.resize(300, 400)

        layout = QVBoxLayout()

        # Product name
        layout.addWidget(QLabel("Product Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        # SKU
        layout.addWidget(QLabel("SKU:"))
        self.sku_input = QLineEdit()
        layout.addWidget(self.sku_input)

        # Category
        layout.addWidget(QLabel("Category:"))
        self.category_dropdown = QComboBox()
        layout.addWidget(self.category_dropdown)

        # Price
        layout.addWidget(QLabel("Price:"))
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(1000000)
        self.price_input.setDecimals(2)
        layout.addWidget(self.price_input)

        # Quantity
        layout.addWidget(QLabel("Quantity in Stock:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1000000)
        layout.addWidget(self.quantity_input)

        # Submit button
        add_button = QPushButton("➕ Add Product")
        add_button.clicked.connect(self.add_product)
        layout.addWidget(add_button)

        self.setLayout(layout)

        self.load_categories()

    def load_categories(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.category_dropdown.clear()
        for cat_id, cat_name in categories:
            self.category_dropdown.addItem(cat_name, cat_id)

    def add_product(self):
        name = self.name_input.text()
        sku = self.sku_input.text()
        category_id = self.category_dropdown.currentData()
        price = self.price_input.value()
        quantity = self.quantity_input.value()

        if not name:
            QMessageBox.warning(self, "Error", "Product name cannot be empty.")
            return

        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, category_id, sku, price, quantity_in_stock)
            VALUES (?, ?, ?, ?, ?)
        """, (name, category_id, sku, price, quantity))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Product added successfully.")
        self.close()
