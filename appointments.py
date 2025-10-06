import sqlite3
from datetime import datetime, timedelta

def connect_db():
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            service TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_appointment(username, name, date, time, service, phone_number):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (username, name, date, time, service, phone_number)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, name, date, time, service, phone_number))
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

def delete_appointment(appointment_id):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
    conn.commit()
    conn.close()

def get_appointments_for_tomorrow():
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, time FROM appointments WHERE date=?", (tomorrow,))
    result = cursor.fetchall()
    conn.close()
    return result

def update_appointment(appointment_id, new_date, new_time):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET date=?, time=? WHERE id=?", (new_date, new_time, appointment_id))
    conn.commit()
    conn.close()

def get_appointments_by_name(name):
    conn = sqlite3.connect("appointments.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, time, service FROM appointments WHERE name=?", (name,))
    result = cursor.fetchall()
    conn.close()
    return result  # [(id, date, time, service)]
