import sqlite3

# Δημιουργεί/συνδέεται με τη βάση
def connect_db():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            username TEXT PRIMARY KEY ,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            service TEXT NOT NULL,
            phone_number TEXT NOT NULL

        )
    """)
    conn.commit()
    conn.close()

def add_appointment(name, date, time, service):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO appointments (name, date, time, service) VALUES (?, ?, ?, ?)",
                   (name, date, time, service))
    conn.commit()
    conn.close()

def get_all_appointments():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments ORDER BY date, time")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_appointments_by_date(date):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT time FROM appointments WHERE date = ?", (date,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_appointments():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments")
    appointments = cursor.fetchall()
    conn.close()
    return appointments

def delete_appointment(appointment_id):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()
