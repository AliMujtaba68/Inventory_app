import os
import shutil
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../db/database.db'))
BACKUP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backups'))

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_database(parent=None):
    if not os.path.exists(DB_PATH):
        QMessageBox.critical(parent, "Error", "Database file not found!")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        shutil.copy2(DB_PATH, backup_path)
        QMessageBox.information(parent, "Backup Successful", f"Backup saved to:\n{backup_path}")
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Backup failed:\n{e}")

def restore_database(parent=None):
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Select Backup File",
        BACKUP_DIR,
        "Database Files (*.db)"
    )
    if not file_path:
        return

    try:
        shutil.copy2(file_path, DB_PATH)
        QMessageBox.information(parent, "Restore Successful", "Database restored from backup.")
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"Restore failed:\n{e}")
