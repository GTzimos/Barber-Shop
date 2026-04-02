from __future__ import annotations

from typing import Callable

from PyQt6.QtWidgets import (
    QFormLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QDialog,
)

from appointments import delete_appointment, get_all_appointments, get_appointments_for_tomorrow
from qt_ui import center_window, make_card_layout, setup_frameless
from services import load_services, save_services
from users import get_user_profile


class AppointmentsDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        center_window(self, 650, 520)
        content = setup_frameless(self, "Όλα τα ραντεβού")
        card = make_card_layout(content)

        self.appointments = get_all_appointments()

        title = QLabel("Ραντεβού")
        title.setObjectName("Heading")
        card.addWidget(title)

        self.list_widget = QListWidget()
        for appointment in self.appointments:
            self.list_widget.addItem(f"{appointment[1]} - {appointment[2]} - {appointment[3]} - {appointment[4]}")
        card.addWidget(self.list_widget)

        cancel_btn = QPushButton("Ακύρωση επιλεγμένου")
        cancel_btn.setObjectName("Danger")
        cancel_btn.clicked.connect(self._cancel_selected)

        profile_btn = QPushButton("Προβολή Προφίλ Πελάτη")
        profile_btn.setObjectName("Secondary")
        profile_btn.clicked.connect(self._view_profile)

        card.addWidget(cancel_btn)
        card.addWidget(profile_btn)

    def _selected_index(self) -> int:
        index = self.list_widget.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return -1
        return index

    def _cancel_selected(self) -> None:
        index = self._selected_index()
        if index < 0:
            return

        confirm = QMessageBox.question(self, "Επιβεβαίωση", "Θέλεις σίγουρα να ακυρώσεις το ραντεβού;")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        delete_appointment(self.appointments[index][0])
        self.list_widget.takeItem(index)
        self.appointments.pop(index)
        QMessageBox.information(self, "Επιτυχία", "Το ραντεβού ακυρώθηκε.")

    def _view_profile(self) -> None:
        index = self._selected_index()
        if index < 0:
            return

        username = self.appointments[index][1]
        profile = get_user_profile(username)
        if not profile:
            QMessageBox.critical(self, "Σφάλμα", "Δεν βρέθηκαν στοιχεία για αυτόν τον πελάτη.")
            return

        name, phone = profile
        QMessageBox.information(self, "Προφίλ Πελάτη", f"Όνομα: {name}\nΤηλέφωνο: {phone}\nUsername: {username}")


class ManagePricesDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        center_window(self, 500, 440)
        content = setup_frameless(self, "Διαχείριση Τιμών")
        card = make_card_layout(content)

        title = QLabel("Διαχείριση Τιμών")
        title.setObjectName("Heading")
        card.addWidget(title)

        self.entries = {}
        form = QFormLayout()
        services = load_services()

        from PyQt6.QtWidgets import QLineEdit

        for service_name, price in services.items():
            field = QLineEdit(str(price))
            form.addRow(service_name, field)
            self.entries[service_name] = field

        card.addLayout(form)

        save_button = QPushButton("Αποθήκευση")
        save_button.setObjectName("Primary")
        save_button.clicked.connect(self._save)
        card.addWidget(save_button)

    def _save(self) -> None:
        try:
            updated = {name: float(field.text()) for name, field in self.entries.items()}
            save_services(updated)
            QMessageBox.information(self, "Επιτυχία", "Οι τιμές αποθηκεύτηκαν.")
            self.accept()
        except ValueError:
            QMessageBox.critical(self, "Σφάλμα", "Μη έγκυρη τιμή.")


class RemindersDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        center_window(self, 680, 500)
        content = setup_frameless(self, "Υπενθυμίσεις Ραντεβού")
        card = make_card_layout(content)

        title = QLabel("Ραντεβού για Αύριο")
        title.setObjectName("Heading")
        card.addWidget(title)

        self.appointment_data = []
        self.list_widget = QListWidget()
        card.addWidget(self.list_widget)

        appointments = get_appointments_for_tomorrow()
        if not appointments:
            empty = QLabel("Δεν υπάρχουν ραντεβού για αύριο.")
            empty.setObjectName("Subtle")
            card.addWidget(empty)
        else:
            for username, time in appointments:
                profile = get_user_profile(username)
                if profile:
                    name, phone = profile
                    display = f"{name} ({username}) - {time} - Τηλ: {phone}"
                    self.appointment_data.append((username, name, phone, time))
                else:
                    display = f"{username} - {time} - [στοιχεία μη διαθέσιμα]"
                    self.appointment_data.append((username, username, "Άγνωστο", time))
                self.list_widget.addItem(display)

        send_button = QPushButton("Αποστολή Υπενθύμισης")
        send_button.setObjectName("Primary")
        send_button.clicked.connect(self._send_reminder)
        card.addWidget(send_button)

    def _send_reminder(self) -> None:
        index = self.list_widget.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return

        username, name, phone, time = self.appointment_data[index]
        QMessageBox.information(
            self,
            "Αποστολή Υπενθύμισης",
            f"Η υπενθύμιση εστάλη επιτυχώς στον {name} ({username}) στο τηλέφωνο {phone} για τις {time}.",
        )


class BarberMenuWindow(QWidget):
    def __init__(self, on_logout: Callable[[], None] | None = None) -> None:
        super().__init__()
        self.on_logout = on_logout

        center_window(self, 560, 420)
        content = setup_frameless(self, "Μενού Κουρέα")
        card = make_card_layout(content)

        heading = QLabel("Barber Dashboard")
        heading.setObjectName("Heading")
        card.addWidget(heading)

        subtitle = QLabel("Είσαι συνδεδεμένος ως κουρέας")
        subtitle.setObjectName("Subtle")
        card.addWidget(subtitle)

        appt_button = QPushButton("Προβολή όλων των ραντεβού")
        appt_button.setObjectName("Primary")
        appt_button.clicked.connect(lambda: AppointmentsDialog(self).exec())

        prices_button = QPushButton("Διαχείριση Τιμών")
        prices_button.setObjectName("Secondary")
        prices_button.clicked.connect(lambda: ManagePricesDialog(self).exec())

        reminders_button = QPushButton("Υπενθυμίσεις Αύριο")
        reminders_button.setObjectName("Secondary")
        reminders_button.clicked.connect(lambda: RemindersDialog(self).exec())

        logout_button = QPushButton("Logout")
        logout_button.setObjectName("Danger")
        logout_button.clicked.connect(self._logout)

        card.addWidget(appt_button)
        card.addWidget(prices_button)
        card.addWidget(reminders_button)
        card.addWidget(logout_button)

    def _logout(self) -> None:
        self.close()
        if self.on_logout:
            self.on_logout()


def open_barber_menu(on_logout: Callable[[], None] | None = None) -> BarberMenuWindow:
    return BarberMenuWindow(on_logout)
