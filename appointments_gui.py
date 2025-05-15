import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from appointments import add_appointment, get_appointments_by_date
from datetime import datetime

class AppointmentWindow:
    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("Κλείσε Ραντεβού")
        self.root.geometry("300x350")
        self.username = username

        # Καλωσόρισμα
        tk.Label(self.root, text=f"Καλώς ήρθες {username}", font=("Arial", 16)).pack(pady=10)

        # Επιλογή Ημερομηνίας
        tk.Label(self.root, text="Ημερομηνία:").pack()
        self.date_entry = DateEntry(self.root, mindate=datetime.today(), date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)
        self.date_entry.bind("<<DateEntrySelected>>", self.update_available_times)

        # Επιλογή Ώρας (θα ενημερωθεί δυναμικά)
        tk.Label(self.root, text="Ώρα:").pack()
        self.time_var = tk.StringVar(self.root)
        self.time_menu = tk.OptionMenu(self.root, self.time_var, "")
        self.time_menu.pack(pady=5)

        # Επιλογή Υπηρεσίας
        tk.Label(self.root, text="Υπηρεσία:").pack()
        self.service_var = tk.StringVar(self.root)
        self.service_var.set("Κούρεμα")
        services = ["Κούρεμα", "Ξύρισμα", "Βαφή", "Ξύρισμα & Κούρεμα"]
        tk.OptionMenu(self.root, self.service_var, *services).pack(pady=5)

        # Κουμπί για υποβολή
        tk.Button(self.root, text="Κλείσε Ραντεβού", command=self.submit_appointment).pack(pady=20)

        self.update_available_times()  # αρχικό γέμισμα ωρών
        self.root.mainloop()

    def update_available_times(self, event=None):
        selected_date = self.date_entry.get()
        all_hours = [f"{h:02}:00" for h in range(9, 21)]  # Ώρες 09:00 - 20:00

        # Αν είναι σήμερα → φιλτράρουμε ώρες που έχουν περάσει
        if selected_date == datetime.today().strftime('%Y-%m-%d'):
            now_hour = datetime.now().hour
            all_hours = [h for h in all_hours if int(h[:2]) > now_hour]

        # Παίρνουμε τις ήδη κλεισμένες ώρες για την ημέρα
        booked = get_appointments_by_date(selected_date)
        booked_hours = [appt[0] for appt in booked]

        available_hours = [h for h in all_hours if h not in booked_hours]

        if not available_hours:
            self.time_var.set("Καμία διαθέσιμη ώρα")
        else:
            self.time_var.set(available_hours[0])

        # Ενημέρωση drop-down
        menu = self.time_menu["menu"]
        menu.delete(0, "end")
        for hour in available_hours:
            menu.add_command(label=hour, command=lambda h=hour: self.time_var.set(h))

    def submit_appointment(self):
        date = self.date_entry.get()
        time = self.time_var.get()
        service = self.service_var.get()

        if time == "Καμία διαθέσιμη ώρα":
            messagebox.showwarning("Μη διαθέσιμο", "Δεν υπάρχουν διαθέσιμες ώρες για την επιλεγμένη ημερομηνία.")
            return

        try:
            add_appointment(self.username, date, time, service)
            messagebox.showinfo("Επιτυχία", "Το ραντεβού καταχωρήθηκε!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα καταχώρησης: {e}")
