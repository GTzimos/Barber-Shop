from __future__ import annotations

from datetime import datetime
from typing import Callable

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QComboBox,
    QCalendarWidget,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMessageBox,
    QPushButton,
    QSlider,
    QWidget,
)

from appointment_editor import AppointmentEditor
from appointments import add_appointment, delete_appointment, get_appointments_by_date, get_appointments_by_name
from qt_ui import center_window, iso_date, make_card_layout, setup_frameless
from ratings import add_rating, get_average_rating
from services import load_services
from users import get_name_by_username, get_user_profile


class RatingDialog(QDialog):
    def __init__(self, username: str, parent=None) -> None:
        super().__init__(parent)
        self.username = username

        center_window(self, 440, 300)
        content = setup_frameless(self, "Αξιολόγηση Υπηρεσίας")
        card = make_card_layout(content)

        heading = QLabel("Αξιολόγηση")
        heading.setObjectName("Heading")
        card.addWidget(heading)

        avg_rating = get_average_rating()
        avg_text = f"Μέση αξιολόγηση: {avg_rating}/5" if avg_rating else "Δεν υπάρχουν αξιολογήσεις ακόμα"
        subtitle = QLabel(avg_text)
        subtitle.setObjectName("Subtle")
        card.addWidget(subtitle)

        card.addWidget(QLabel("Βαθμολόγησε την εμπειρία σου:"))
        self.slider = QSlider()
        self.slider.setOrientation(self.slider.orientation().Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(5)
        self.slider.setValue(5)
        card.addWidget(self.slider)

        self.rating_label = QLabel("5 / 5")
        self.rating_label.setObjectName("Field")
        card.addWidget(self.rating_label)
        self.slider.valueChanged.connect(lambda value: self.rating_label.setText(f"{value} / 5"))

        submit_button = QPushButton("Υποβολή Αξιολόγησης")
        submit_button.setObjectName("Primary")
        submit_button.clicked.connect(self._submit)
        card.addWidget(submit_button)

    def _submit(self) -> None:
        try:
            add_rating(self.username, self.slider.value())
            QMessageBox.information(self, "Ευχαριστούμε", "Η αξιολόγηση αποθηκεύτηκε!")
            self.accept()
        except Exception as error:  # noqa: BLE001
            QMessageBox.critical(self, "Σφάλμα", f"Σφάλμα αποθήκευσης αξιολόγησης: {error}")


class AppointmentCancelerDialog(QDialog):
    def __init__(self, username: str, parent=None) -> None:
        super().__init__(parent)
        center_window(self, 520, 420)

        content = setup_frameless(self, "Ακύρωση Ραντεβού")
        card = make_card_layout(content)

        title = QLabel("Τα ραντεβού σου")
        title.setObjectName("Heading")
        card.addWidget(title)

        name = get_name_by_username(username)
        self.appointments = get_appointments_by_name(name) if name else []

        self.list_widget = QListWidget()
        for appointment in self.appointments:
            self.list_widget.addItem(f"{appointment[1]} - {appointment[2]} ({appointment[3]})")
        card.addWidget(self.list_widget)

        cancel_button = QPushButton("Ακύρωση Επιλεγμένου")
        cancel_button.setObjectName("Danger")
        cancel_button.clicked.connect(self._cancel_selected)
        card.addWidget(cancel_button)

    def _cancel_selected(self) -> None:
        selected_index = self.list_widget.currentRow()
        if selected_index < 0:
            QMessageBox.warning(self, "Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return

        confirm = QMessageBox.question(self, "Επιβεβαίωση", "Είσαι σίγουρος ότι θέλεις να ακυρώσεις το ραντεβού;")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        appointment_id = self.appointments[selected_index][0]
        delete_appointment(appointment_id)
        QMessageBox.information(self, "Επιτυχία", "Το ραντεβού ακυρώθηκε.")
        self.accept()


class AppointmentWindow(QWidget):
    def __init__(self, username: str, on_logout: Callable[[], None] | None = None) -> None:
        super().__init__()
        self.username = username
        self.on_logout = on_logout
        self.services = load_services()

        center_window(self, 760, 760)
        content = setup_frameless(self, "Κλείσε Ραντεβού")
        card = make_card_layout(content)

        heading = QLabel(f"Γεια σου, {username}")
        heading.setObjectName("Heading")
        card.addWidget(heading)

        subtitle = QLabel("Οργάνωσε το επόμενο ραντεβού σου σε λίγα δευτερόλεπτα.")
        subtitle.setObjectName("Subtle")
        card.addWidget(subtitle)

        quick_actions = QHBoxLayout()

        edit_button = QPushButton("Τροποποίηση Ραντεβού")
        edit_button.setObjectName("Secondary")
        edit_button.clicked.connect(self._open_editor)

        cancel_button = QPushButton("Ακύρωση Ραντεβού")
        cancel_button.setObjectName("Danger")
        cancel_button.clicked.connect(self._open_canceler)

        quick_actions.addWidget(edit_button)
        quick_actions.addWidget(cancel_button)
        card.addLayout(quick_actions)

        calendar_label = QLabel("Ημερολόγιο Ραντεβού")
        calendar_label.setObjectName("Field")
        card.addWidget(calendar_label)

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setMinimumDate(QDate.currentDate())
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self._on_calendar_changed)
        card.addWidget(self.calendar)

        details_grid = QGridLayout()
        details_grid.setHorizontalSpacing(8)
        details_grid.setVerticalSpacing(4)

        selected_title = QLabel("Επιλεγμένη ημέρα")
        selected_title.setObjectName("Subtle")
        self.selected_date_label = QLabel()
        self.selected_date_label.setObjectName("Field")

        slots_title = QLabel("Διαθέσιμες ώρες")
        slots_title.setObjectName("Subtle")
        self.slots_label = QLabel()
        self.slots_label.setObjectName("Field")

        details_grid.addWidget(selected_title, 0, 0)
        details_grid.addWidget(self.selected_date_label, 1, 0)
        details_grid.addWidget(slots_title, 0, 1)
        details_grid.addWidget(self.slots_label, 1, 1)
        card.addLayout(details_grid)

        card.addWidget(QLabel("Ώρα"))
        self.time_combo = QComboBox()
        card.addWidget(self.time_combo)

        card.addWidget(QLabel("Υπηρεσία"))
        self.service_combo = QComboBox()
        self.service_combo.addItems([f"{name} - {price}EUR" for name, price in self.services.items()])
        card.addWidget(self.service_combo)

        submit_button = QPushButton("Κλείσε Ραντεβού")
        submit_button.setObjectName("Primary")
        submit_button.clicked.connect(self.submit_appointment)
        card.addWidget(submit_button)

        logout_button = QPushButton("Logout")
        logout_button.setObjectName("Secondary")
        logout_button.clicked.connect(self.logout_user)
        card.addWidget(logout_button)

        self._on_calendar_changed()

    def _open_editor(self) -> None:
        editor = AppointmentEditor(self.username, self)
        if editor.exec():
            self.update_available_times()

    def _open_canceler(self) -> None:
        dialog = AppointmentCancelerDialog(self.username, self)
        if dialog.exec():
            self.update_available_times()

    def logout_user(self) -> None:
        self.close()
        if self.on_logout:
            self.on_logout()

    def _on_calendar_changed(self) -> None:
        selected_date = self.calendar.selectedDate().toString("dd/MM/yyyy")
        self.selected_date_label.setText(selected_date)
        self.update_available_times()

    def update_available_times(self) -> None:
        selected_date = iso_date(self.calendar.selectedDate())
        all_hours = [f"{hour:02}:00" for hour in range(9, 21)]

        if selected_date == datetime.today().strftime("%Y-%m-%d"):
            now_hour = datetime.now().hour
            all_hours = [hour for hour in all_hours if int(hour[:2]) > now_hour]

        booked = get_appointments_by_date(selected_date)
        booked_hours = [appointment[0] for appointment in booked]
        available_hours = [hour for hour in all_hours if hour not in booked_hours]

        self.time_combo.clear()
        if available_hours:
            self.time_combo.addItems(available_hours)
            self.slots_label.setText(str(len(available_hours)))
        else:
            self.time_combo.addItem("Καμία διαθέσιμη ώρα")
            self.slots_label.setText("0")

    def submit_appointment(self) -> None:
        date = iso_date(self.calendar.selectedDate())
        time = self.time_combo.currentText()
        service = self.service_combo.currentText().split(" - ")[0]

        if time == "Καμία διαθέσιμη ώρα":
            QMessageBox.warning(self, "Μη διαθέσιμο", "Δεν υπάρχουν διαθέσιμες ώρες για την επιλεγμένη ημερομηνία.")
            return

        profile = get_user_profile(self.username)
        if not profile:
            QMessageBox.critical(self, "Σφάλμα", "Δεν βρέθηκαν στοιχεία χρήστη.")
            return

        name, phone = profile
        try:
            add_appointment(self.username, name, date, time, service, phone)
            QMessageBox.information(self, "Επιτυχία", "Το ραντεβού καταχωρήθηκε!")
            self.update_available_times()
            rating = RatingDialog(self.username, self)
            if rating.exec():
                self.close()
                if self.on_logout:
                    self.on_logout()
        except Exception as error:  # noqa: BLE001
            QMessageBox.critical(self, "Σφάλμα", f"Σφάλμα καταχώρησης: {error}")
