from login import open_login_window
from users import connect_db
from barber_menu import open_barber_menu
from appointments_gui import AppointmentWindow
from appointments import connect_db as connect_appointments_db
from ratings import connect_db as connect_ratings_db  # Νέα εισαγωγή

def on_login_success(username):
    if username == "admin":
        open_barber_menu()
    else:
        AppointmentWindow(username)

def main():
    connect_db()  # Βάση χρηστών
    connect_appointments_db()  # Βάση ραντεβού
    connect_ratings_db()  # Βάση αξιολογήσεων
    open_login_window(on_login_success)

if __name__ == "__main__":
    main()