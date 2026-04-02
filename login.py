from __future__ import annotations

from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)

from qt_ui import center_window, make_card_layout, setup_frameless
from users import open_register_window, verify_user


class LoginWindow(QWidget):
    def __init__(self, on_login_success: Callable[[str], None]) -> None:
        super().__init__()
        self.on_login_success = on_login_success

        center_window(self, 500, 380)
        content = setup_frameless(self, "Barber Hub")
        card = make_card_layout(content)

        heading = QLabel("Barber Shop")
        heading.setObjectName("Heading")
        card.addWidget(heading)

        subtitle = QLabel("Κάνε σύνδεση για να διαχειριστείς το επόμενο ραντεβού σου.")
        subtitle.setWordWrap(True)
        subtitle.setObjectName("Subtle")
        card.addWidget(subtitle)

        form = QGridLayout()
        form.setHorizontalSpacing(10)
        form.setVerticalSpacing(8)

        user_label = QLabel("Username")
        user_label.setObjectName("Field")
        self.username_input = QLineEdit()

        pass_label = QLabel("Password")
        pass_label.setObjectName("Field")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form.addWidget(user_label, 0, 0)
        form.addWidget(self.username_input, 1, 0)
        form.addWidget(pass_label, 2, 0)
        form.addWidget(self.password_input, 3, 0)
        card.addLayout(form)

        actions = QHBoxLayout()
        login_button = QPushButton("Σύνδεση")
        login_button.setObjectName("Primary")
        login_button.clicked.connect(self._handle_login)

        register_button = QPushButton("Εγγραφή")
        register_button.setObjectName("Secondary")
        register_button.clicked.connect(self._open_register)

        actions.addWidget(login_button)
        actions.addWidget(register_button)
        card.addLayout(actions)

        self.username_input.setFocus()

    def _handle_login(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Προσοχή", "Συμπλήρωσε username και password.")
            return

        user = verify_user(username, password)
        if not user:
            QMessageBox.critical(self, "Σφάλμα", "Λάθος στοιχεία!")
            return

        QMessageBox.information(self, "Επιτυχία", f"Καλώς ήρθες {username}!")
        self.close()
        self.on_login_success(username)

    def _open_register(self) -> None:
        open_register_window(self)

    def keyPressEvent(self, event) -> None:  # noqa: N802
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._handle_login()
            return
        super().keyPressEvent(event)


def open_login_window(on_success: Callable[[str], None]) -> LoginWindow:
    return LoginWindow(on_success)
