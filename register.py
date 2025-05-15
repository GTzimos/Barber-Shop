# register.py

import tkinter as tk
from tkinter import messagebox
from users import add_user  # Εισάγουμε τη συνάρτηση για προσθήκη χρήστη

def open_register_window(root):
    # Δημιουργία νέου παραθύρου για εγγραφή
    register_window = tk.Toplevel(root)  # Δημιουργεί ένα νέο παράθυρο (Toplevel)
    register_window.title("Εγγραφή Χρήστη")
    
    # Ετικέτες και πεδία εισαγωγής για εγγραφή
    tk.Label(register_window, text="Username:").pack(pady=10)
    entry_username = tk.Entry(register_window)
    entry_username.pack()
    
    tk.Label(register_window, text="Password:").pack(pady=10)
    entry_password = tk.Entry(register_window, show="*")
    entry_password.pack()
    
    tk.Label(register_window, text="Name:").pack(pady=10)
    entry_name = tk.Entry(register_window)
    entry_name.pack()
    
    tk.Label(register_window, text="Phone Number:").pack(pady=10)
    entry_phone_number = tk.Entry(register_window)
    entry_phone_number.pack()

    # Συνάρτηση για καταχώρηση χρήστη
    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        name = entry_name.get()
        phone_number = entry_phone_number.get()

        try:
            add_user(username, password, name, phone_number)
            messagebox.showinfo("Επιτυχία", "Ο χρήστης εγγράφηκε επιτυχώς!")
            register_window.destroy()  # Κλείσιμο παραθύρου μετά την εγγραφή
        except ValueError as e:
            messagebox.showerror("Σφάλμα", "sads")

    # Κουμπί για εγγραφή χρήστη
    register_button = tk.Button(register_window, text="Register", command=register_user)
    register_button.pack(pady=20)
