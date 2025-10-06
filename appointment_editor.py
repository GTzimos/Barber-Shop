import tkinter as tk
from tkcalendar import DateEntry
from appointments import get_appointments_by_name, update_appointment, get_appointments_by_date
from datetime import datetime

class AppointmentEditor:
    def __init__(self, username):
        self.username = username
        self.root = tk.Toplevel()
        self.root.title("Τροποποίηση Ραντεβού")
        self.root.geometry("400x400")

        tk.Label(self.root, text="Τα ραντεβού σου:", font=("Arial", 12)).pack(pady=5)

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=5)

        from users import get_name_by_username
        name = get_name_by_username(username)
        self.appointments = get_appointments_by_name(name)

        for app in self.appointments:
            text = f"{app[1]} - {app[2]} ({app[3]})"
            self.listbox.insert(tk.END, text)

        tk.Label(self.root, text="Νέα Ημερομηνία:").pack()
        self.date_entry = DateEntry(self.root, mindate=datetime.today(), date_pattern='yyyy-mm-dd')
        self.date_entry.pack()

        tk.Label(self.root, text="Νέα Ώρα:").pack()
        self.time_var = tk.StringVar()
        self.time_menu = tk.OptionMenu(self.root, self.time_var, "")
        self.time_menu.pack()

        self.date_entry.bind("<<DateEntrySelected>>", self.load_available_times)

        tk.Button(self.root, text="Αποθήκευση Αλλαγής", command=self.save_changes).pack(pady=10)


    def load_available_times(self, event=None):
        selected_date = self.date_entry.get()
        all_hours = [f"{h:02}:00" for h in range(9, 21)]
        booked = get_appointments_by_date(selected_date)
        booked_hours = [b[0] for b in booked]
        available = [h for h in all_hours if h not in booked_hours]

        menu = self.time_menu["menu"]
        menu.delete(0, "end")
        for h in available:
            menu.add_command(label=h, command=lambda v=h: self.time_var.set(v))

        if available:
            self.time_var.set(available[0])
        else:
            self.time_var.set("Καμία διαθέσιμη ώρα")

    def save_changes(self):
        idx = self.listbox.curselection()
        if not idx:
            tk.messagebox.showwarning("Σφάλμα", "Δεν επιλέχθηκε ραντεβού.")
            return

        new_date = self.date_entry.get()
        new_time = self.time_var.get()

        if new_time == "Καμία διαθέσιμη ώρα":
            tk.messagebox.showerror("Σφάλμα", "Δεν υπάρχουν διαθέσιμες ώρες.")
            return

        appointment_id = self.appointments[idx[0]][0]
        update_appointment(appointment_id, new_date, new_time)

        tk.messagebox.showinfo("Επιτυχία", "Το ραντεβού ενημερώθηκε.")
        self.root.destroy()
