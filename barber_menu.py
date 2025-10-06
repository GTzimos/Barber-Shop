import tkinter as tk
from services import load_services, save_services
from appointments import get_all_appointments, delete_appointment,get_appointments_for_tomorrow
from users import get_user_profile  
from tkinter import messagebox


def open_barber_menu():
    root = tk.Tk()
    root.title("Μενού Κουρέα")

    tk.Label(root, text="Είσαι συνδεδεμένος ως Κουρέας", font=("Arial", 16)).pack(pady=20)

    # Προσθήκη λειτουργιών κουρέα (π.χ. Προβολή όλων των ραντεβού)
    tk.Button(root, text="Προβολή όλων των ραντεβού", command=show_appointments).pack(pady=10)
    
    tk.Button(root, text="Διαχείριση Τιμών", command=manage_prices).pack(pady=10)
    
    tk.Button(root, text="Υπενθυμίσεις Αύριο", command=show_reminders).pack(pady=5)

    # Κουμπί Logout
    def handle_logout():
        from logout import logout
        logout(root) # Καλεί τη συνάρτηση με το root του παραθύρου

    tk.Button(root, text="Logout", command=handle_logout).pack(pady=20)
  
    root.mainloop()

def show_appointments():
    window = tk.Toplevel()
    window.title("Όλα τα ραντεβού")
    window.geometry("400x400")

    tk.Label(window, text="Ραντεβού", font=("Arial", 14)).pack(pady=10)

    listbox = tk.Listbox(window, width=50)
    listbox.pack(pady=10)

    appointments = get_all_appointments()
    for app in appointments:
        display = f"{app[1]} - {app[2]} - {app[3]} - {app[4]}"  # username - date - time - service
        listbox.insert(tk.END, display)

    def cancel_selected():
        selected = listbox.curselection()
        if not selected:
            tk.messagebox.showwarning("Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return
        confirm = tk.messagebox.askyesno("Επιβεβαίωση", "Θέλεις σίγουρα να ακυρώσεις το ραντεβού;")
        if confirm:
            index = selected[0]
            appointment = appointments[index]
            delete_appointment(appointment[0])  # Χρήση ID αν υπάρχει
            listbox.delete(index)
            tk.messagebox.showinfo("Επιτυχία", "Το ραντεβού ακυρώθηκε.")

    def view_profile():
        selected = listbox.curselection()
        if not selected:
            tk.messagebox.showwarning("Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return
        index = selected[0]
        username = appointments[index][1]
        profile = get_user_profile(username)
        if profile:
            name, phone = profile
            info = f"Όνομα: {name}\nΤηλέφωνο: {phone}\nUsername: {username}"
            tk.messagebox.showinfo("Προφίλ Πελάτη", info)
        else:
            tk.messagebox.showerror("Σφάλμα", "Δεν βρέθηκαν στοιχεία για αυτόν τον πελάτη.")

    tk.Button(window, text="Ακύρωση επιλεγμένου", command=cancel_selected).pack(pady=5)
    tk.Button(window, text="Προβολή Προφίλ Πελάτη", command=view_profile).pack(pady=5)
    

def manage_prices():
    window = tk.Toplevel()
    window.title("Διαχείριση Τιμών")

    services = load_services()
    entries = {}

    for i, (name, price) in enumerate(services.items()):
        tk.Label(window, text=name).grid(row=i, column=0, padx=10, pady=5)
        e = tk.Entry(window)
        e.insert(0, str(price))
        e.grid(row=i, column=1)
        entries[name] = e

    def save():
        try:
            updated = {name: float(entry.get()) for name, entry in entries.items()}
            save_services(updated)
            tk.messagebox.showinfo("Επιτυχία", "Οι τιμές αποθηκεύτηκαν.")
            window.destroy()
        except ValueError:
            tk.messagebox.showerror("Σφάλμα", "Μη έγκυρη τιμή.")

    tk.Button(window, text="Αποθήκευση", command=save).grid(row=len(services), column=0, columnspan=2, pady=10)
    
    

def show_reminders():
    window = tk.Toplevel()
    window.title("Υπενθυμίσεις Ραντεβού για Αύριο")
    window.geometry("500x400")

    tk.Label(window, text="Ραντεβού για Αύριο", font=("Arial", 14)).pack(pady=10)

    appointments = get_appointments_for_tomorrow()

    if not appointments:
        tk.Label(window, text="Δεν υπάρχουν ραντεβού για αύριο.").pack(pady=20)
        return

    listbox = tk.Listbox(window, width=60)
    listbox.pack(pady=10)

    appointment_data = []

    for i, (username, time) in enumerate(appointments):
        profile = get_user_profile(username)
        if profile:
            name, phone = profile
            display = f"{name} ({username}) - {time} - Τηλ: {phone}"
            appointment_data.append((username, name, phone, time))
        else:
            display = f"{username} - {time} - [στοιχεία μη διαθέσιμα]"
            appointment_data.append((username, username, "Άγνωστο", time))

        listbox.insert(tk.END, display)

    def send_reminder():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Προσοχή", "Δεν επιλέχθηκε ραντεβού.")
            return

        index = selection[0]
        username, name, phone, time = appointment_data[index]

        # Εδώ θα εμφανιστεί το μήνυμα επιτυχίας
        messagebox.showinfo("Αποστολή Υπενθύμισης", f"Η υπενθύμιση εστάλη επιτυχώς στον {name} ({username}) στο τηλέφωνο {phone} για τις {time}.")

    tk.Button(window, text="Αποστολή Υπενθύμισης", command=send_reminder).pack(pady=10)
