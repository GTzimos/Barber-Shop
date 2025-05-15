import tkinter as tk
from appointments import get_all_appointments, delete_appointment
def open_barber_menu():
    root = tk.Tk()
    root.title("Μενού Κουρέα")

    tk.Label(root, text="Είσαι συνδεδεμένος ως Κουρέας", font=("Arial", 16)).pack(pady=20)

    # Προσθήκη λειτουργιών κουρέα (π.χ. Προβολή όλων των ραντεβού)
    tk.Button(root, text="Προβολή όλων των ραντεβού", command=show_appointments).pack(pady=10)


    root.mainloop()

def show_appointments():
    window = tk.Toplevel()
    window.title("Όλα τα ραντεβού")
    window.geometry("400x400")

    tk.Label(window, text="Ραντεβού", font=("Arial", 14)).pack(pady=10)

    listbox = tk.Listbox(window, width=50)
    listbox.pack(pady=10)

    # Φόρτωση όλων των ραντεβού
    appointments = get_all_appointments()
    for app in appointments:
        display = f"{app[1]} - {app[2]} - {app[3]} - {app[4]}"
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
            delete_appointment(appointment[0])  # Χρησιμοποιεί το ID
            listbox.delete(index)
            tk.messagebox.showinfo("Επιτυχία", "Το ραντεβού ακυρώθηκε.")

    tk.Button(window, text="Ακύρωση επιλεγμένου", command=cancel_selected).pack(pady=10)
