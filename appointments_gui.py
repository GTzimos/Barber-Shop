import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from appointments import add_appointment, get_appointments_by_date
from datetime import datetime
from services import load_services
from appointment_editor import AppointmentEditor
from users import get_user_profile
from appointments import get_appointments_by_name, delete_appointment
from ratings import add_rating, get_average_rating

class AppointmentWindow:

    def __init__(self, username):
        self.root = tk.Tk()
        self.root.title("Κλείσε Ραντεβού")
        self.root.geometry("350x500")
        self.username = username

        # Καλωσόρισμα
        tk.Label(self.root, text=f"Καλώς ήρθες {username}", font=("Arial", 16)).pack(pady=10)

        # ΤΡΟΠΟΠΟΙΗΣΗ ΡΑΝΤΕΒΟΥ
        tk.Button(self.root, text="Τροποποίηση Ραντεβού", command=lambda: AppointmentEditor(self.username)).pack(pady=6)

        tk.Button(self.root, text="Ακύρωση Ραντεβού", command=lambda: AppointmentCanceler(self.username)).pack(pady=5)

        tk.Label(self.root, text="Δεν έχεις Ραντεβού; Κλείσε!").pack()

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
        services = load_services()  
        tk.Label(self.root, text="Υπηρεσία:").pack() 
        self.service_var = tk.StringVar(self.root)
        first_service = list(services.keys())[0]
        self.service_var.set(first_service)

        def format_service(s):
            return f"{s} - {services[s]}€"

        options = list(map(format_service, services.keys()))
        self.service_menu = tk.OptionMenu(self.root, self.service_var, *options)
        self.service_menu.pack(pady=5)

        # Κουμπί για υποβολή
        tk.Button(self.root, text="Κλείσε Ραντεβού", command=self.submit_appointment).pack(pady=20)
        
        # Κουμπί Logout
        tk.Button(self.root, text="Logout", command=self.logout_user).pack(pady=10) 

        self.update_available_times()  # αρχικό γέμισμα ωρών
        self.root.mainloop()

    def logout_user(self):
        from logout import logout
        logout(self.root)

    def update_available_times(self, event=None):
        selected_date = self.date_entry.get()
        all_hours = [f"{h:02}:00" for h in range(9, 21)]

        if selected_date == datetime.today().strftime('%Y-%m-%d'):
            now_hour = datetime.now().hour
            all_hours = [h for h in all_hours if int(h[:2]) > now_hour]

        booked = get_appointments_by_date(selected_date)
        booked_hours = [appt[0] for appt in booked]

        available_hours = [h for h in all_hours if h not in booked_hours]

        if not available_hours:
            self.time_var.set("Καμία διαθέσιμη ώρα")
        else:
            self.time_var.set(available_hours[0])

        menu = self.time_menu["menu"]
        menu.delete(0, "end")
        for hour in available_hours:
            menu.add_command(label=hour, command=lambda h=hour: self.time_var.set(h))

    def submit_appointment(self):
        date = self.date_entry.get()
        time = self.time_var.get()
        service_full = self.service_var.get()
        service = service_full.split(" - ")[0]

        if time == "Καμία διαθέσιμη ώρα":
            messagebox.showwarning("Μη διαθέσιμο", "Δεν υπάρχουν διαθέσιμες ώρες για την επιλεγμένη ημερομηνία.")
            return

        profile = get_user_profile(self.username)
        if profile:
            name, phone = profile
        else:
            messagebox.showerror("Σφάλμα", "Δεν βρέθηκαν στοιχεία χρήστη.")
            return

        try:
            add_appointment(self.username, name, date, time, service, phone)
            messagebox.showinfo("Επιτυχία", "Το ραντεβού καταχωρήθηκε!")
            self.open_rating_window()
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Σφάλμα καταχώρησης: {e}")

    def open_rating_window(self):
        rating_window = tk.Toplevel(self.root)
        rating_window.title("Αξιολόγηση Υπηρεσίας")
        rating_window.geometry("350x280")
        rating_window.transient(self.root)
        rating_window.grab_set()

        # Εμφάνιση μέσης αξιολόγησης
        avg_rating = get_average_rating()
        if avg_rating:
            rating_text = f"Μέση αξιολόγηση: {avg_rating}/5 ⭐"
        else:
            rating_text = "Δεν υπάρχουν αξιολογήσεις ακόμα"
        
        tk.Label(rating_window, text=rating_text, font=("Arial", 12)).pack(pady=10)
        tk.Label(rating_window, text="Βαθμολόγησε την εμπειρία σου:", font=("Arial", 12)).pack(pady=10)

        rating_var = tk.IntVar()
        rating_var.set(5)

        # Δημιουργία κουμπιών αστεριών
        stars_frame = tk.Frame(rating_window)
        stars_frame.pack()

        def set_rating(value):
            rating_var.set(value)
            for i in range(5):
                if i < value:
                    star_buttons[i].config(text="★", fg="gold")
                else:
                    star_buttons[i].config(text="☆", fg="gray")

        star_buttons = []
        for i in range(1, 6):
            star_btn = tk.Button(stars_frame, text="☆", font=("Arial", 20), fg="gray",
                               command=lambda v=i: set_rating(v))
            star_btn.pack(side=tk.LEFT)
            star_buttons.append(star_btn)

        set_rating(5)

        def submit_rating():
            rating = rating_var.get()
            try:
                add_rating(self.username, rating)
                messagebox.showinfo("Ευχαριστούμε", "Η αξιολόγηση αποθηκεύτηκε!")
                rating_window.destroy()
                self.root.destroy()
            except Exception as e:
                messagebox.showerror("Σφάλμα", f"Σφάλμα αποθήκευσης αξιολόγησης: {e}")

        tk.Button(rating_window, text="Υποβολή Αξιολόγησης", command=submit_rating, 
                 bg="green", fg="white", font=("Arial", 12)).pack(pady=15)

class AppointmentCanceler:
    def __init__(self, username):
        self.username = username
        self.root = tk.Toplevel()
        self.root.title("Ακύρωση Ραντεβού")
        self.root.geometry("400x400")

        from users import get_name_by_username
        name = get_name_by_username(username)
        self.appointments = get_appointments_by_name(name)

        tk.Label(self.root, text="Τα ραντεβού σου:", font=("Arial", 12)).pack(pady=10)

        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)

        for app in self.appointments:
            self.listbox.insert(tk.END, f"{app[1]} - {app[2]} ({app[3]})")

        tk.Button(self.root, text="Ακύρωση Επιλεγμένου", command=self.cancel_selected).pack(pady=10)

    def cancel_selected(self):
        idx = self.listbox.curselection()
        if not idx:
            tk.messagebox.showwarning("Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return

        confirm = tk.messagebox.askyesno("Επιβεβαίωση", "Είσαι σίγουρος ότι θέλεις να ακυρώσεις το ραντεβού;")
        if confirm:
            appointment_id = self.appointments[idx[0]][0]
            delete_appointment(appointment_id)
            tk.messagebox.showinfo("Επιτυχία", "Το ραντεβού ακυρώθηκε.")
            self.root.destroy()