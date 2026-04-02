from __future__ import annotations

import re
import sqlite3

from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from qt_ui import center_window, make_card_layout, setup_frameless

DB_FILE = "users.db"


def connect_db() -> None:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username_db TEXT UNIQUE NOT NULL,
            password_db TEXT NOT NULL,
            name_db TEXT NOT NULL,
            phone_number_db TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def verify_user(username: str, password: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username_db=? AND password_db=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user


def add_user(username: str, password: str, name: str, phone_number: str) -> None:
    if not re.match(r"^\d{10}$", phone_number):
        raise ValueError("Το τηλέφωνο πρέπει να έχει 10 ψηφία.")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username_db, password_db, name_db, phone_number_db) VALUES (?, ?, ?, ?)",
            (username, password, name, phone_number),
        )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        raise ValueError("Το όνομα χρήστη υπάρχει ήδη.") from exc
    finally:
        conn.close()


class RegisterDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        center_window(self, 520, 440)
        content = setup_frameless(self, "Εγγραφή Χρήστη")
        card = make_card_layout(content)

        heading = QLabel("Νέος Λογαριασμός")
        heading.setObjectName("Heading")
        card.addWidget(heading)

        subtitle = QLabel("Συμπλήρωσε τα στοιχεία σου για γρήγορη κράτηση.")
        subtitle.setObjectName("Subtle")
        card.addWidget(subtitle)

        form = QFormLayout()
        form.setVerticalSpacing(8)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()

        form.addRow("Username", self.username_input)
        form.addRow("Password", self.password_input)
        form.addRow("Full Name", self.name_input)
        form.addRow("Phone Number", self.phone_input)
        card.addLayout(form)

        actions = QVBoxLayout()
        submit = QPushButton("Ολοκλήρωση Εγγραφής")
        submit.setObjectName("Primary")
        submit.clicked.connect(self._register)

        cancel = QPushButton("Ακύρωση")
        cancel.setObjectName("Secondary")
        cancel.clicked.connect(self.reject)

        actions.addWidget(submit)
        actions.addWidget(cancel)
        card.addLayout(actions)

        self.username_input.setFocus()

    def _register(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        name = self.name_input.text().strip()
        phone_number = self.phone_input.text().strip()

        if not all([username, password, name, phone_number]):
            QMessageBox.warning(self, "Προσοχή", "Συμπλήρωσε όλα τα πεδία.")
            return

        try:
            add_user(username, password, name, phone_number)
            QMessageBox.information(self, "Επιτυχία", "Ο χρήστης εγγράφηκε επιτυχώς!")
            self.accept()
        except ValueError as error:
            QMessageBox.critical(self, "Σφάλμα", str(error))


def open_register_window(parent=None) -> int:
    dialog = RegisterDialog(parent)
    return dialog.exec()


def get_user_profile(username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name_db, phone_number_db FROM users WHERE username_db=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result


def get_name_by_username(username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name_db FROM users WHERE username_db=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
