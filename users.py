import sqlite3
import re
import tkinter as tk
from tkinter import messagebox

DB_FILE = "users.db"  # Κοινή χρήση σταθεράς αρχείου

def connect_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username_db TEXT PRIMARY KEY,
            password_db TEXT NOT NULL,
            name_db TEXT NOT NULL,
            phone_number_db TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username_db=? AND password_db=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Πρέπει να επιστρέφει τα στοιχεία χρήστη ή None αν δεν βρεθεί


def add_user(username, password, name, phone_number):
    if not re.match(r"^\d{10}$", phone_number):
        raise ValueError("Το τηλέφωνο πρέπει να έχει 10 ψηφία.")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username_db, password_db, name_db, phone_number_db) VALUES (?, ?, ?, ?)",
                       (username, password, name, phone_number))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Το όνομα χρήστη υπάρχει ήδη.")
    finally:
        conn.close()

def open_register_window(root):
    register_window = tk.Toplevel(root)
    register_window.title("Εγγραφή Χρήστη")
    
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

    def register_user():
        username = entry_username.get()
        password = entry_password.get()
        name = entry_name.get()
        phone_number = entry_phone_number.get()

        try:
            add_user(username, password, name, phone_number)
            messagebox.showinfo("Επιτυχία", "Ο χρήστης εγγράφηκε επιτυχώς!")
            register_window.destroy()
        except ValueError as e:
            messagebox.showerror("Σφάλμα", str(e))

    tk.Button(register_window, text="Εγγραφή", command=register_user).pack(pady=10)
