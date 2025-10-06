import os
import sqlite3

def reset_database():
    # Λίστα αρχείων βάσης δεδομένων προς διαγραφή
    db_files = ["users.db", "appointments.db", "ratings.db"]
    
    for db_file in db_files:
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"Διεγράφη: {db_file}")
        else:
            print(f"Δεν βρέθηκε: {db_file}")
    
    # Δημιουργία νέας βάσης users με default admin
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username_db TEXT UNIQUE NOT NULL,
            password_db TEXT NOT NULL,
            name_db TEXT NOT NULL,
            phone_number_db TEXT NOT NULL
        )
    """)
    
    # Προσθήκη default admin (password: admin123)
    try:
        cursor.execute(
            "INSERT INTO users (username_db, password_db, name_db, phone_number_db) VALUES (?, ?, ?, ?)",
            ("admin", "admin123", "Κύριος Κουρέας", "1234567890")
        )
        print("Δημιουργήθηκε default admin: username=admin, password=admin123")
    except sqlite3.IntegrityError:
        print("Ο admin υπάρχει ήδη")
    
    conn.commit()
    conn.close()
    
    print("Η βάση δεδομένων επαναφέρθηκε successfully!")

if __name__ == "__main__":
    reset_database()