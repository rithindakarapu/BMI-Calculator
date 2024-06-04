import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib import pyplot as plt
from datetime import datetime

# Database setup
conn = sqlite3.connect('bmi_data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL)''')
conn.commit()

# Function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height / 100) ** 2, 2)

# Function to categorize BMI
def categorize_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# Function to save BMI data
def save_bmi_data(name, weight, height, bmi, category):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO bmi_records (name, weight, height, bmi, category, date) VALUES (?, ?, ?, ?, ?, ?)",
                   (name, weight, height, bmi, category, date))
    conn.commit()

# Function to display historical data
def show_history():
    cursor.execute("SELECT date, bmi FROM bmi_records WHERE name=?", (name_entry.get(),))
    records = cursor.fetchall()
    
    if not records:
        messagebox.showinfo("Info", "No historical data found.")
        return
    
    dates = [datetime.strptime(record[0], "%Y-%m-%d %H:%M:%S") for record in records]
    bmis = [record[1] for record in records]
    
    plt.figure("BMI History")
    plt.plot_date(dates, bmis, '-o')
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title(f"BMI History for {name_entry.get()}")
    plt.gcf().autofmt_xdate()
    plt.show()

# Function to handle BMI calculation
def handle_calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        name = name_entry.get()
        
        if not name:
            raise ValueError("Name cannot be empty")
        
        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive numbers")
        
        bmi = calculate_bmi(weight, height)
        category = categorize_bmi(bmi)
        
        result_label.config(text=f"BMI: {bmi} ({category})")
        
        save_bmi_data(name, weight, height, bmi, category)
        
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))

# Setup GUI
root = tk.Tk()
root.title("BMI Calculator")

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Weight (kg)").grid(row=1, column=0)
tk.Label(root, text="Height (cm)").grid(row=2, column=0)

name_entry = tk.Entry(root)
weight_entry = tk.Entry(root)
height_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
weight_entry.grid(row=1, column=1)
height_entry.grid(row=2, column=1)

calculate_button = tk.Button(root, text="Calculate BMI", command=handle_calculate)
calculate_button.grid(row=3, column=0, columnspan=2)

history_button = tk.Button(root, text="Show History", command=show_history)
history_button.grid(row=4, column=0, columnspan=2)

result_label = tk.Label(root, text="BMI: ")
result_label.grid(row=5, column=0, columnspan=2)

root.mainloop()

# Close database connection when the app is closed
conn.close()
