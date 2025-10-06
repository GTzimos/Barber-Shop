# Barbershop Appointment Management System

## Project Context
**This project was developed as a group assignment by 3 students for educational purposes** (specifically for a university or college course). It serves to demonstrate the implementation of a full-stack desktop application using Python, GUI programming (Tkinter), and database integration.

---

## Project Description
This is a desktop application developed in **Python** using the **Tkinter** library for the Graphical User Interface (GUI) and **SQLite** for database management. The system is designed to streamline the process of scheduling, managing, and tracking appointments for a barbershop, offering separate interfaces for customers and barbers/administrators.

---

## Key Features

The application provides the following core functionalities:

### Customer Features
* **User Authentication:** Secure **Login** and **Registration** for new customers (`login.py`, `register.py`).
* **Appointment Booking:** Schedule new appointments by selecting date, time, and service (`appointments_gui.py`).
* **Appointment Management:** View, **Edit** (`appointment_editor.py`), and **Cancel** existing appointments (`appointments_gui.py`).
* **Service Rating:** Submit a **Rating** (1-5 stars) for the service received (`ratings.py`, `appointments_gui.py`).
* **Logout** (`logout.py`).

### Barber/Admin Features (User: 'admin')
* **View All Appointments:** See a list of all scheduled appointments (`barber_menu.py`).
* **Price Management:** **Manage** (add, edit, delete) the list of available services and their prices, stored in `services.json` (`barber_menu.py`, `services.py`).
* **Appointment Reminders:** View **Reminders** for appointments scheduled for the next day, including customer contact details (`barber_menu.py`).
* **Logout** (`logout.py`).

---

## Technical Details and Files

### Database Structure
The application uses **SQLite** databases for persistent storage:
* `users.db`: Stores customer/admin login credentials and contact information.
* `appointments.db`: Stores all scheduled appointments (who, when, what service).
* `ratings.db`: Stores user ratings for the barbershop.

### Core Files

| File Name | Description |
| :--- | :--- |
| `main.py` | The main application entry point. Initializes all databases and launches the login window. |
| `login.py` | Handles user sign-in and directs to the appropriate user interface. |
| `register.py` | GUI and logic for new customer registration. |
| `users.py` | Database functions for managing user accounts and retrieving profiles (`users.db`). |
| `appointments_gui.py` | The main customer interface for booking, cancelling, and rating. |
| `barber_menu.py` | The administrator's menu for managing appointments, prices, and reminders. |
| `appointments.py` | Database functions for managing appointments (`appointments.db`). |
| `ratings.py` | Database functions for storing and calculating the average rating (`ratings.db`). |
| `services.py` | Functions to load and save service prices from `services.json`. |
| `services.json` | JSON file containing a list of services and their current prices. |
| `dada.py` | Utility script to **reset all databases** and create the default admin account for testing. |

---

## Getting Started

### Prerequisites

To run this application, you need to have **Python 3.x** installed.

The required external Python library is:
* `tkcalendar`

You can install it using pip:
```bash
pip install tkcalendar
