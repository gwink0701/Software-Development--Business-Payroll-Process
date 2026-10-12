# Pseudo Squad - Group Project - Payroll Management System
# ================================================
# 1. IMPORT SECTION
# ================================================
import tkinter as tk #<-- This line imports the tkinter module and gives it the alias 'tk', which is used to create GUI elements in Python
from tkinter import messagebox, ttk #<-- This line imports themed widgets and message boxes from tkinter
import hashlib  #<-- This line imports the hashlib module, which is used for secure password hashing
import os #<-- This line imports the os module, which provides functions for interacting with the operating system, such as file and directory management
import csv  #<--- This line imports the csv module, which is used for reading from and writing to CSV files

# ============================================================
# 2. AUTHORIZED USERS
# ============================================================
# Passwords are stored as SHA-256 hashes rather than
# plain-text passwords to satisfy security requirements.

AUTHORIZED_USERS = {
    "admin": hashlib.sha256("Admin123!".encode()).hexdigest(),
    "payroll": hashlib.sha256("Payroll123!".encode()).hexdigest(),
    "user": hashlib.sha256("User123!".encode()).hexdigest(),
} #<--

# ================================================
# 3. Employee Database
# ================================================
EMPLOYEES = { #<-- This line defines a dictionary called EMPLOYEES that contains employee information, where each key is an employee ID and the value is another dictionary with details about the employee
    4821: {#<-- This line defines an entry in the EMPLOYEES dictionary for an employee with ID 4821
        "name": "Liam Carter",#<-- This line specifies the name of the employee as "Liam Carter"
        "hourly_rate": 23,#<-- This line specifies the hourly rate of the employee as 23
        "dependents": 2,#<-- This line specifies the number of dependents for the employee as 2
        "regular_hours": 40,#<-- This line specifies the number of regular hours worked by the employee as 40
        "overtime_hours": 3.5
    },

    7395: {
        "name": "Olivia Bennett",
        "hourly_rate": 19,
        "dependents": 0,
        "regular_hours": 38,
        "overtime_hours": 0
    },

    1648: {
        "name": "Noah Sullivan",
        "hourly_rate": 26,
        "dependents": 3,
        "regular_hours": 40,
        "overtime_hours": 6
    },

    9072: {
        "name": "Emma Rodriguez",
        "hourly_rate": 21,
        "dependents": 1,
        "regular_hours": 40,
        "overtime_hours": 0
    },

    3514: {
        "name": "Ethan Walker",
        "hourly_rate": 28,
        "dependents": 4,
        "regular_hours": 40,
        "overtime_hours": 8.5
    },

    6283: {
        "name": "Ava Mitchell",
        "hourly_rate": 23,
        "dependents": 2,
        "regular_hours": 36.5,
        "overtime_hours": 0
    },

    8457: {
        "name": "Mason Foster",
        "hourly_rate": 17,
        "dependents": 0,
        "regular_hours": 40,
        "overtime_hours": 2
    },

    2936: {
        "name": "Isabella Hayes",
        "hourly_rate": 24,
        "dependents": 1,
        "regular_hours": 39.5,
        "overtime_hours": 0
    },

    5701: {
        "name": "Lucas Bennett",
        "hourly_rate": 31,
        "dependents": 3,
        "regular_hours": 40,
        "overtime_hours": 10
    },

    7164: {
        "name": "Sophia Nguyen",
        "hourly_rate": 20,
        "dependents": 2,
        "regular_hours": 40,
        "overtime_hours": 4
    }
}

# UI by Greg A. Watkins II
# Create the main window and shared visual styles.
window = tk.Tk() 
window.title("Pseudo Squad | Payroll Management System")
window.configure(bg="#F3F6F3")
window.resizable(True, True)

background = "#F3F6F3"
surface = "#FFFFFF"
text_color = "#20302C"
muted_color = "#64736D"
accent = "#2E6B5E"
accent_hover = "#24584D"

style = ttk.Style(window)
style.theme_use("clam")
style.configure("TLabel", background=surface, foreground=text_color, font=("Segoe UI", 10))
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"))
style.configure("Subtitle.TLabel", foreground=muted_color, font=("Segoe UI", 10))
style.configure("Field.TLabel", font=("Segoe UI", 10, "bold"))
style.configure("TEntry", fieldbackground=surface, foreground=text_color, padding=(10, 9),
                bordercolor="#CBD7D0", lightcolor="#CBD7D0", darkcolor="#CBD7D0")
style.map("TEntry", bordercolor=[("focus", accent)], lightcolor=[("focus", accent)],
          darkcolor=[("focus", accent)])
style.configure("Primary.TButton", background=accent, foreground="#FFFFFF",
                font=("Segoe UI", 10, "bold"), padding=(18, 10), borderwidth=0)
style.map("Primary.TButton", background=[("active", accent_hover), ("pressed", accent_hover)])
style.configure("Secondary.TButton", background="#E5ECE7", foreground=text_color,
                font=("Segoe UI", 10, "bold"), padding=(18, 10), borderwidth=0)
style.map("Secondary.TButton", background=[("active", "#D8E2DB")])

def center_window(width, height):
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

center_window(440, 500)

# Login screen shown before the payroll interface.
login_frame = tk.Frame(window, bg=background)
login_frame.pack(fill="both", expand=True)

login_panel = tk.Frame(login_frame, bg=surface, padx=36, pady=34,
                       highlightbackground="#DCE5DE", highlightthickness=1)
login_panel.place(relx=0.5, rely=0.5, anchor="center", width=360)

ttk.Label(login_panel, text="Pseudo Squad", style="Subtitle.TLabel").pack(anchor="w")
ttk.Label(login_panel, text="Payroll", style="Title.TLabel").pack(anchor="w", pady=(4, 3))
ttk.Label(login_panel, text="Sign in to continue", style="Subtitle.TLabel").pack(anchor="w", pady=(0, 24))

ttk.Label(login_panel, text="Username", style="Field.TLabel").pack(anchor="w", pady=(0, 6))
username_entry = ttk.Entry(login_panel, font=("Segoe UI", 11))
username_entry.pack(fill="x")

ttk.Label(login_panel, text="Password", style="Field.TLabel").pack(anchor="w", pady=(17, 6))
password_entry = ttk.Entry(login_panel, show="*", font=("Segoe UI", 11))
password_entry.pack(fill="x")

login_button = ttk.Button(login_panel, text="Sign in", style="Primary.TButton", command=lambda: login())
login_button.pack(fill="x", pady=(26, 0))

payroll_frame = tk.Frame(window, bg=background, padx=40, pady=32)
payroll_frame.columnconfigure(0, weight=1)

payroll_header = tk.Frame(payroll_frame, bg=background)
payroll_header.grid(row=0, column=0, sticky="ew", pady=(0, 25))
ttk.Label(payroll_header, text="Payroll Management", style="Title.TLabel").pack(anchor="w")
ttk.Label(payroll_header, text="Enter employee details to process payroll", style="Subtitle.TLabel").pack(anchor="w", pady=(4, 0))

employee_form = tk.Frame(payroll_frame, bg=surface, padx=26, pady=26,
                         highlightbackground="#DCE5DE", highlightthickness=1)
employee_form.grid(row=1, column=0, sticky="ew")
employee_form.columnconfigure(0, weight=1, uniform="fields")
employee_form.columnconfigure(1, weight=1, uniform="fields")

ttk.Label(employee_form, text="Employee ID", style="Field.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 18), pady=(0, 7))
employee_id = ttk.Entry(employee_form, font=("Segoe UI", 11))
employee_id.grid(row=1, column=0, sticky="ew", padx=(0, 18), pady=(0, 20))

ttk.Label(employee_form, text="Employee Name", style="Field.TLabel").grid(row=0, column=1, sticky="w", pady=(0, 7))
employee_name = ttk.Entry(employee_form, font=("Segoe UI", 11))
employee_name.grid(row=1, column=1, sticky="ew", pady=(0, 20))

ttk.Label(employee_form, text="Number of Dependents", style="Field.TLabel").grid(row=2, column=0, sticky="w", padx=(0, 18), pady=(0, 7))
dependents = ttk.Entry(employee_form, font=("Segoe UI", 11))
dependents.grid(row=3, column=0, sticky="ew", padx=(0, 18))

ttk.Label(employee_form, text="Hours Worked", style="Field.TLabel").grid(row=2, column=1, sticky="w", pady=(0, 7))
hours_worked = ttk.Entry(employee_form, font=("Segoe UI", 11))
hours_worked.grid(row=3, column=1, sticky="ew")

ttk.Label(employee_form, text="Hourly Rate ($)", style="Field.TLabel").grid(row=4, column=0, sticky="w", padx=(0, 18), pady=(20, 7))
hourly_rate=ttk.Entry(employee_form, font=("Segoe UI", 11))
hourly_rate.grid(row=5, column=0, sticky="ew", padx=(0, 18))

payroll_actions = tk.Frame(payroll_frame, bg=background)
payroll_actions.grid(row=2, column=0, sticky="e", pady=(22, 0))


def login():
    username = username_entry.get().strip()
    password = password_entry.get()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    if not username or not password:
        messagebox.showwarning(
            "Login Required",
            "Enter both a username and password."
        )
    elif username not in AUTHORIZED_USERS or password_hash != AUTHORIZED_USERS[username]:
        messagebox.showerror("Login Failed", "Invalid username or password.")
    else:
        login_frame.pack_forget()
        center_window(920, 580)
        window.resizable(True, True)
        window.minsize(760, 500)
        payroll_frame.pack(fill="both", expand=True)

# Calculations
# (Ian) 9/27/2026

def calculate_payroll(employee_number, hours, hourly_rate):
    # Tax rates
    Federal_Tax_Rate = 0.079
    State_Tax_Rate = 0.056

    # Calculate regular and overtime hours
    regular_hours = min(hours, 40)
    overtime_hours = max(hours - 40, 0)

    # Calculate gross pay
    regular_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * (hourly_rate * 1.5)
    pre_tax_pay = regular_pay + overtime_pay

    # Calculate tax deductions
    fed_tax_deduction = pre_tax_pay * Federal_Tax_Rate
    state_tax_deduction = pre_tax_pay * State_Tax_Rate
    total_deductions = fed_tax_deduction + state_tax_deduction

    # Calculate net pay
    post_tax_pay = pre_tax_pay - total_deductions

    return {
        "employee_number": employee_number,
        "regular_hours": regular_hours,
        "overtime_hours": overtime_hours,
        "regular_pay": regular_pay,
        "overtime_pay": overtime_pay,
        "pre_tax_pay": pre_tax_pay,
        "fed_tax_deduction": fed_tax_deduction,
        "state_tax_deduction": state_tax_deduction,
        "total_deductions": total_deductions,
        "post_tax_pay": post_tax_pay
    }

username_entry.bind("<Return>", lambda event: password_entry.focus_set())
password_entry.bind("<Return>", lambda event: login())
username_entry.focus_set()

# Load employee information automatically

def load_employee():
    employee_number = employee_id.get().strip()

    if not employee_number:
        messagebox.showwarning(
            "Missing Employee ID",
            "Please enter an Employee ID first."
        )
        return

    try:
        employee_number = int(employee_number)
    except ValueError:
        messagebox.showerror(
            "Invalid Employee ID",
            "Employee ID must be a whole number."
        )
        return

    employee = EMPLOYEES.get(employee_number)

    if employee is None:
        messagebox.showerror(
            "Employee Not Found",
            "That Employee ID is not in the database."
        )
        return

    employee_name.delete(0, tk.END)
    employee_name.insert(0, employee["name"])

    dependents.delete(0, tk.END)
    dependents.insert(0, employee["dependents"])

    hourly_rate.delete(0, tk.END)
    hourly_rate.insert(0, employee["hourly_rate"])

    default_hours = employee["regular_hours"] + employee["overtime_hours"]

    hours_worked.delete(0, tk.END)
    hours_worked.insert(0, default_hours)

def save_payroll(
    employee_number,
    employee_name_value,
    pre_tax_pay,
    state_tax_deduction,
    fed_tax_deduction,
    post_tax_pay
):
    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "employee_paychecks.csv"
    )

    # Check whether the file exists and contains data
    file_exists = os.path.exists(filename)
    file_is_empty = not file_exists or os.path.getsize(filename) == 0

    with open(filename, mode="a", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Write headers if the file is new or empty
        if file_is_empty:
            writer.writerow([
                "Employee ID",
                "Employee Name",
                "Gross Pay",
                "State Tax Deductions",
                "Federal Tax Deductions",
                "Net Pay"
            ])

        # Write payroll information
        writer.writerow([
            employee_number,
            employee_name_value,
            f"{pre_tax_pay:.2f}",
            f"{state_tax_deduction:.2f}",
            f"{fed_tax_deduction:.2f}",
            f"{post_tax_pay:.2f}"
        ])

    print("Payroll saved successfully!")
    print("File location:", os.path.abspath(filename))
    print("File size:", os.path.getsize(filename), "bytes")

    return filename


def enter_employee():
    employee_number_text = employee_id.get().strip()
    name = employee_name.get().strip()
    number_dependents_text = dependents.get().strip()
    hours_text = hours_worked.get().strip()
    hourly_rate_text = hourly_rate.get().strip()

    try:
        employee_number = int(employee_number_text)
        number_dependents = int(number_dependents_text)
        hours = float(hours_text)
        hourly_rate_value = float(hourly_rate_text)

    except ValueError:
        messagebox.showerror(
            "Invalid information",
            "Employee ID and dependents must be whole numbers.\n"
            "Hours worked and hourly rate must be numbers."
        )
        return

    if employee_number not in EMPLOYEES:
        messagebox.showerror(
            "Employee Not Found",
            "That Employee ID is not in the employee database."
        )
        return

    correct_name = EMPLOYEES[employee_number]["name"]
    normalized_name = " ".join(name.casefold().split())
    normalized_correct_name = " ".join(correct_name.casefold().split())

    if normalized_name != normalized_correct_name:
        warning = (
            f"Employee name spelling mismatch for Employee ID {employee_number}.\n"
            f"Entered name: {name}\n"
            f"Correct spelling: {correct_name}"
        )
        print(f"WARNING: {warning}")
        messagebox.showwarning(
            "Employee Name Mismatch",
            f"{warning}\n\nCorrect the employee name before processing payroll."
        )
        return

    if hours < 0:
        messagebox.showerror(
            "Invalid Hours",
            "Hours worked cannot be negative."
        )
        return

    if hourly_rate_value < 0:
        messagebox.showerror(
            "Invalid Hourly Rate",
            "Hourly rate cannot be negative."
        )
        return

    if number_dependents < 0:
        messagebox.showerror(
            "Invalid Dependents",
            "Number of dependents cannot be negative."
        )
        return

    payroll = calculate_payroll(employee_number, hours, hourly_rate_value)
    pre_tax_pay = payroll["pre_tax_pay"]
    state_tax_deduction = payroll["state_tax_deduction"]
    fed_tax_deduction = payroll["fed_tax_deduction"]
    post_tax_pay = payroll["post_tax_pay"]

    print()
    print("\nEmployee Pay Information")
    print("--------------------------------------")
    print("Employee ID:", employee_number)
    print("Employee name:", name)
    print("Dependents:", number_dependents)
    print("Hours Worked:", hours)
    print("Hourly Rate: $", format(hourly_rate_value, ".2f"))
    print("Regular Pay: $", format(payroll["regular_pay"], ".2f"))
    print("Overtime Pay: $", format(payroll["overtime_pay"], ".2f"))
    print("Gross Pay: $", format(pre_tax_pay, ".2f"))
    print("State Tax Deductions $:", format(state_tax_deduction, ".2f"))
    print("Federal Tax Deductions: $", format(fed_tax_deduction, ".2f"))
    print("Total Deductions: $", format(payroll["total_deductions"], ".2f"))
    print("Net Pay: $", format(post_tax_pay, ".2f"))

    try:
        filename = save_payroll(
            employee_number,
            name,
            pre_tax_pay,
            state_tax_deduction,
            fed_tax_deduction,
            post_tax_pay
        )
    except Exception as error:
        messagebox.showerror("Spreadsheet Error", f"Could not save payroll information:\n{error}")
        return

    messagebox.showinfo(
        "Payroll Complete",
        f"Payroll processed successfully!\n\n"
        f"Employee: {name}\n"
        f"Employee ID: {employee_number}\n\n"
        f"Gross Pay: ${pre_tax_pay:.2f}\n"
        f"State Tax: ${state_tax_deduction:.2f}\n"
        f"Federal Tax: ${fed_tax_deduction:.2f}\n"
        f"Net Pay: ${post_tax_pay:.2f}\n\n"
        f"Saved to:\n{filename}"
    )
 
def cancel():
    """
    Ask the user for confirmation before exiting.
    """

    if messagebox.askyesno(
        "Cancel",
        "Are you sure you want to cancel?\n\n"
        "This action will exit the program."
    ):
        window.destroy()

payroll_actions = tk.Frame(
    payroll_frame,
    bg=background
)

payroll_actions.grid(
    row=2,
    column=0,
    sticky="e",
    pady=(22, 0)
)


# Load employee button

load_button = ttk.Button(
    payroll_actions,
    text="Load Employee",
    command=load_employee,
    style="Secondary.TButton"
)

load_button.pack(
    side="left",
    padx=(0, 12)
)


# Process payroll button

enter_button = ttk.Button(
    payroll_actions,
    text="Process Payroll",
    command=enter_employee,
    style="Primary.TButton"
)

enter_button.pack(
    side="left",
    padx=(0, 12)
)


# Clear button

def clear_form():
    employee_id.delete(0, tk.END)
    employee_name.delete(0, tk.END)
    dependents.delete(0, tk.END)
    hours_worked.delete(0, tk.END)
    hourly_rate.delete(0, tk.END)

    employee_id.focus_set()

clear_button = ttk.Button(
    payroll_actions,
    text="Clear",
    command=clear_form,
    style="Secondary.TButton"
)

clear_button.pack(
    side="left",
    padx=(0, 12)
)


# Cancel button

cancel_button = ttk.Button(
    payroll_actions,
    text="Cancel",
    command=cancel,
    style="Secondary.TButton"
)

cancel_button.pack(
    side="left"
)


# Start the program
window.resizable(False, False) 
window.mainloop()