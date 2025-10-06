import tkinter as tk
from tkinter import messagebox
from users import verify_user, open_register_window
from appointments_gui import AppointmentWindow
from barber_menu import open_barber_menu

def open_login_window(on_success):
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("300x250")

    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()

        user = verify_user(username, password)
        if user:
            messagebox.showinfo("Επιτυχία", f"Καλώς ήρθες {username}!")

            def proceed():
                login_window.destroy()
                on_success(username)

            login_window.after(100, proceed)
        else:
            messagebox.showerror("Σφάλμα", "Λάθος στοιχεία!")

    tk.Button(login_window, text="Login", command=handle_login).pack(pady=10)
    tk.Button(login_window, text="Εγγραφή", command=lambda: open_register_window(login_window)).pack(pady=10)

    login_window.mainloop()
