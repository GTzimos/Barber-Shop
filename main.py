from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from appointments import connect_db as connect_appointments_db
from appointments_gui import AppointmentWindow
from barber_menu import BarberMenuWindow
from login import LoginWindow
from qt_ui import apply_app_style
from ratings import connect_db as connect_ratings_db
from users import connect_db


class AppController:
    def __init__(self) -> None:
        self.current_window = None

    def show_login(self) -> None:
        self._replace_window(LoginWindow(self._on_login_success))

    def _on_login_success(self, username: str) -> None:
        if username == "admin":
            self._replace_window(BarberMenuWindow(self.show_login))
            return

        self._replace_window(AppointmentWindow(username, self.show_login))

    def _replace_window(self, window) -> None:
        if self.current_window is not None:
            self.current_window.close()
        self.current_window = window
        self.current_window.show()


def main() -> int:
    connect_db()
    connect_appointments_db()
    connect_ratings_db()

    app = QApplication(sys.argv)
    apply_app_style(app)

    controller = AppController()
    controller.show_login()

    return app.exec()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nΗ εφαρμογή τερματίστηκε από τον χρήστη (Ctrl+C).")
