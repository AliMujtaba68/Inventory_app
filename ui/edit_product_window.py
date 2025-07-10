from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox
)
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import db_manager


class EditProductWindow(QWidget):
    def __init__(self, product_id, parent):
        super().__init__()
        self.setWindowTitle("Edit Product")
        self.resize(300, 400)
        self.product_id = product_id
        self.parent = parent  # reference to ViewProductsWindow to refresh the table after editing

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Product Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("SKU:"))
        self.sku_input = QLineEdit()
        layout.addWidget(self.sku_input)

        layout.addWidget(QLabel("Category:"))
        self.category_dropdown = QComboBox()
        layout.addWidget(self.category_dropdown)

        layout.addWidget(QLabel("Price:"))
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(1000000)
        self.price_input.setDecimals(2)
        layout.addWidget(self.price_input)

        layout.addWidget(QLabel("Quantity in Stock:"))
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(1000000)
        layout.addWidget(self.quantity_input)

        save_button = QPushButton("💾 Save Changes")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

        self.setLayout(layout)

        self.load_categories()
        self.load_product_data()

    def load_categories(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.category_dropdown.clear()
        for cat_id, cat_name in categories:
            self.category_dropdown.addItem(cat_name, cat_id)

    def load_product_data(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, category_id, sku, price, quantity_in_stock
            FROM products
            WHERE id=?
        """, (self.product_id,))
        product = cursor.fetchone()
        conn.close()

        if product:
            self.name_input.setText(product[0])
            idx = self.category_dropdown.findData(product[1])
            if idx >= 0:
                self.category_dropdown.setCurrentIndex(idx)
            self.sku_input.setText(product[2])
            self.price_input.setValue(product[3])
            self.quantity_input.setValue(product[4])

    def save_changes(self):
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
            UPDATE products
            SET name=?, category_id=?, sku=?, price=?, quantity_in_stock=?
            WHERE id=?
        """, (name, category_id, sku, price, quantity, self.product_id))
        conn.commit()
        conn.close()

        # Log it
        db_manager.log_action("admin", "Edited", name)

        QMessageBox.information(self, "Success", "Product updated successfully.")
        self.parent.load_products()  # refresh products table
        self.close()
