import tkinter as tk
import sqlite3
from datetime import datetime, timedelta
from tkinter import messagebox
#from thinter import messagebox

# Initialize GUI
root = tk.Tk()
root.title("Student Attendance System")

# Initialize Database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance
                (student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_number TEXT,
                student_payroll TEXT,
                student_name TEXT,
                student_email TEXT,
                arrival_time DATETIME,
                day_of_week TEXT,
                arrival_status TEXT)''')

conn.commit()

# Create GUI components
serial_label = tk.Label(root, text="Scan Serial Number:")
serial_entry = tk.Entry(root)

name_label = tk.Label(root, text="Student Name:")
name_entry = tk.Entry(root)

roll_label = tk.Label(root, text="Payroll:")
name_entry = tk.Entry(root)

email_label = tk.Label(root, text="Student Email:")
email_entry = tk.Entry(root)

mark_present_button = tk.Button(root, text="Mark Present")
review_button = tk.Button(root, text="Review Attendance")
print_button = tk.Button(root, text="Print Attendance")

# Layout components
serial_label.pack()
serial_entry.pack()

name_label.pack()
name_entry.pack()

email_label.pack()
email_entry.pack()

mark_present_button.pack()
review_button.pack()
print_button.pack()


# Function to mark attendance
def mark_present():
    valid_serial_numbers = ["st0001", "st0002", "st0003", "st0004", "st0005", "st0006", "st0007", "st0008"]
    serial_number = serial_entry.get()
    student_name = name_entry.get()
    student_email = email_entry.get()

    if serial_number in valid_serial_numbers:
        current_time = datetime.now()
        arrival_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        day_of_week = current_time.strftime('%A')

        if current_time.time() >= datetime.strptime("08:01:00", "%H:%M:%S").time():
            arrival_status = "Late (Come Late)"
        else:
            arrival_status = "On Time (Come on Time)"

        cursor.execute(
            "INSERT INTO attendance (serial_number, student_name, student_email, arrival_time, day_of_week, arrival_status) VALUES (?, ?, ?, ?, ?, ?)",
            (serial_number, student_name, student_email, arrival_time, day_of_week, arrival_status))
        conn.commit()
        serial_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        messsagebox.showinfo("Succefully", "The student with serial", serial_number, "is marked present")
    else:
        messagebox.showerror("Error", "Invalid serial number we have not assigned any student this serial number.")

# Function to review attendance
def review_attendance():
    review_window = tk.Toplevel(root)
    review_window.title("Review Attendance")

    listbox = tk.Listbox(review_window, width=80)
    listbox.pack()

    cursor.execute(
        "SELECT serial_number, student_name, student_email, arrival_time, day_of_week, arrival_status FROM attendance")
    attendance_data = cursor.fetchall()

    for data in attendance_data:
        listbox.insert(tk.END,
                       f"Serial Number: {data[0]}, Name: {data[1]}, Email: {data[2]}, Arrival Time: {data[3]}, Day: {data[4]}, Status: {data[5]}")


# Function to print attendance
def print_attendance():
    current_date = datetime.now().strftime('%Y-%m-%d')
    report_filename = f"attendance_report_{current_date}.txt"

    with open(report_filename, "w") as file:
        cursor.execute(
            "SELECT serial_number, student_name, student_email, arrival_time, day_of_week, arrival_status FROM attendance")
        attendance_data = cursor.fetchall()
        file.write("Attendance Report\n")
        file.write("=" * 80 + "\n")
        for data in attendance_data:
            file.write(
                f"Serial Number: {data[0]}, Name: {data[1]}, Email: {data[2]}, Arrival Time: {data[3]}, Day: {data[4]}, Status: {data[5]}\n")
        file.write("=" * 80 + "\n")


mark_present_button.config(command=mark_present)
review_button.config(command=review_attendance)
print_button.config(command=print_attendance)

# Run the application
root.mainloop()

# Close the database connection when the application is closed
conn.close()
