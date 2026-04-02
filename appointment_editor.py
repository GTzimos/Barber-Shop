from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QComboBox, QDateEdit, QDialog, QLabel, QListWidget, QMessageBox, QPushButton, QVBoxLayout

from appointments import get_appointments_by_date, get_appointments_by_name, update_appointment
from qt_ui import iso_date, make_card_layout, setup_frameless
from users import get_name_by_username


class AppointmentEditor(QDialog):
    def __init__(self, username: str, parent=None) -> None:
        super().__init__(parent)
        content = setup_frameless(self, "Τροποποίηση Ραντεβού")
        card = make_card_layout(content)

        self.username = username
        name = get_name_by_username(username)
        self.appointments = get_appointments_by_name(name) if name else []

        card.addWidget(QLabel("Τα ραντεβού σου"))
        self.list_widget = QListWidget()
        for appointment in self.appointments:
            self.list_widget.addItem(f"{appointment[1]} - {appointment[2]} ({appointment[3]})")
        card.addWidget(self.list_widget)

        card.addWidget(QLabel("Νέα Ημερομηνία"))
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setMinimumDate(QDate.currentDate())
        self.date_edit.dateChanged.connect(self.load_available_times)
        card.addWidget(self.date_edit)

        card.addWidget(QLabel("Νέα Ώρα"))
        self.time_combo = QComboBox()
        card.addWidget(self.time_combo)

        save_button = QPushButton("Αποθήκευση Αλλαγής")
        save_button.setObjectName("Primary")
        save_button.clicked.connect(self.save_changes)
        card.addWidget(save_button)

        self.load_available_times()

    def load_available_times(self) -> None:
        selected_date = iso_date(self.date_edit.date())
        all_hours = [f"{hour:02}:00" for hour in range(9, 21)]
        booked = get_appointments_by_date(selected_date)
        booked_hours = [entry[0] for entry in booked]
        available = [hour for hour in all_hours if hour not in booked_hours]

        if selected_date == datetime.today().strftime("%Y-%m-%d"):
            now_hour = datetime.now().hour
            available = [hour for hour in available if int(hour[:2]) > now_hour]

        self.time_combo.clear()
        if available:
            self.time_combo.addItems(available)
        else:
            self.time_combo.addItem("Καμία διαθέσιμη ώρα")

    def save_changes(self) -> None:
        selected_index = self.list_widget.currentRow()
        if selected_index < 0:
            QMessageBox.warning(self, "Σφάλμα", "Δεν επιλέχθηκε ραντεβού.")
            return

        new_time = self.time_combo.currentText()
        if new_time == "Καμία διαθέσιμη ώρα":
            QMessageBox.warning(self, "Σφάλμα", "Δεν υπάρχουν διαθέσιμες ώρες.")
            return

        appointment_id = self.appointments[selected_index][0]
        update_appointment(appointment_id, iso_date(self.date_edit.date()), new_time)
        QMessageBox.information(self, "Επιτυχία", "Το ραντεβού ενημερώθηκε.")
        self.accept()
