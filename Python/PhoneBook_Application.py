import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import re

def create_table():
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                category TEXT,
                photo TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print(f"Database created or connected successfully at: {db_path}")
    except sqlite3.Error as e:
        print("Error creating or connecting to database:", e)

def main():
    global name_entry, phone_entry, email_entry, category_var, contacts_listbox, window

    window = tk.Tk()
    window.title("Phonebook Application")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 440
    window_height = 460
    x_coord = (screen_width / 2) - (window_width / 2)
    y_coord = (screen_height / 2) - (window_height / 2)
    window.geometry(f"{window_width}x{window_height}+{int(x_coord)}+{int(y_coord)}")

    tk.Label(window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Phone:").grid(row=1, column=0)
    phone_entry = tk.Entry(window)
    phone_entry.grid(row=1, column=1)

    tk.Label(window, text="Email:").grid(row=2, column=0)
    email_entry = tk.Entry(window)
    email_entry.grid(row=2, column=1)

    tk.Label(window, text="Category:").grid(row=3, column=0)
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(window, textvariable=category_var, values=["Family", "Friends", "Work", "General"])
    category_dropdown.grid(row=3, column=1)

    add_button = tk.Button(window, text="Add", command=lambda: add_contact(name_entry.get(), phone_entry.get(), email_entry.get(), category_var.get()))
    add_button.grid(row=4, column=0, sticky="ew")

    update_button = tk.Button(window, text="Update", command=update_selected_contact)
    update_button.grid(row=4, column=1, sticky="ew")

    delete_button = tk.Button(window, text="Delete", command=lambda: delete_contact(on_select()))
    delete_button.grid(row=4, column=2, sticky="ew")

    clear_button = tk.Button(window, text="Clear Entries", command=clear_entries)
    clear_button.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    exit_button = tk.Button(window, text="Exit", command=window.destroy)
    exit_button.grid(row=5, column=2, pady=10, sticky="ew")

    contacts_listbox = tk.Listbox(window, width=70, height=10)
    contacts_listbox.grid(row=6, column=0, columnspan=3, padx=10, pady=10)
    contacts_listbox.bind('<<ListboxSelect>>', on_select)

    populate_listbox()

    tk.Label(window, text="Search:").grid(row=7, column=0)
    search_entry = tk.Entry(window)
    search_entry.grid(row=7, column=1)
    search_button = tk.Button(window, text="Search", command=lambda: search_contact(search_entry.get()))
    search_button.grid(row=7, column=2)

    sort_by_name_button = tk.Button(window, text="Sort by Name", command=lambda: sort_contacts('name'))
    sort_by_name_button.grid(row=8, column=0)

    sort_by_phone_button = tk.Button(window, text="Sort by Phone", command=lambda: sort_contacts('phone'))
    sort_by_phone_button.grid(row=8, column=1)

    theme_label = tk.Label(window, text="Select Theme:")
    theme_label.grid(row=9, column=0)
    theme_var = tk.StringVar()
    theme_dropdown = ttk.Combobox(window, textvariable=theme_var, values=["Light", "Dark"])
    theme_dropdown.grid(row=9, column=1)
    theme_dropdown.set("Light")
    theme_button = tk.Button(window, text="Apply Theme", command=lambda: change_theme(theme_var.get()))
    theme_button.grid(row=9, column=2)

    upload_button = tk.Button(window, text="Upload Photo", command=upload_photo)
    upload_button.grid(row=10, column=0, columnspan=3, pady=10, sticky="ew")

    window.mainloop()

def add_contact(name, phone, email, category):
    if not name or not phone or not email:
        print("All fields are required.")
        return
    if not is_valid_phone(phone):
        print("Invalid phone number.")
        return
    if not is_valid_email(email):
        print("Invalid email address.")
        return
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, phone, email, category) VALUES (?, ?, ?, ?)",
                       (name, phone, email, category))
        conn.commit()
        conn.close()
        print("Contact added successfully.")
        populate_listbox()
        clear_entries()
    except sqlite3.Error as e:
        print("Error adding contact:", e)

def search_contact(query):
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?",
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        contacts = cursor.fetchall()
        conn.close()
        contacts_listbox.delete(0, tk.END)
        for contact in contacts:
            contacts_listbox.insert(tk.END, f"{contact[0]} - {contact[1]} - {contact[2]} - {contact[3]} - {contact[4]}")
    except sqlite3.Error as e:
        print("Error searching contacts:", e)

def sort_contacts(sort_by):
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM contacts ORDER BY {sort_by}")
        contacts = cursor.fetchall()
        conn.close()
        contacts_listbox.delete(0, tk.END)
        for contact in contacts:
            contacts_listbox.insert(tk.END, f"{contact[0]} - {contact[1]} - {contact[2]} - {contact[3]} - {contact[4]}")
    except sqlite3.Error as e:
        print("Error sorting contacts:", e)

def view_contacts():
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()
        return contacts
    except sqlite3.Error as e:
        print("Error retrieving contacts:", e)
        return []

def update_contact(contact_id, name, phone, email, category):
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE contacts SET name=?, phone=?, email=?, category=? WHERE id=?",
                       (name, phone, email, category, contact_id))
        conn.commit()
        conn.close()
        print("Contact updated successfully.")
        populate_listbox()
        clear_entries()
    except sqlite3.Error as e:
        print("Error updating contact:", e)

def delete_contact(contact_id):
    if contact_id is None:
        print("No contact selected for deletion.")
        return
    try:
        project_folder = r"C:\Users\Gabriel\Projects\Python"
        db_path = os.path.join(project_folder, "Projects.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
        conn.commit()
        conn.close()
        print("Contact deleted successfully.")
        populate_listbox()
        clear_entries()
    except sqlite3.Error as e:
        print("Error deleting contact:", e)

def populate_listbox():
    contacts_listbox.delete(0, tk.END)
    contacts = view_contacts()
    for contact in contacts:
        contacts_listbox.insert(tk.END, f"{contact[0]} - {contact[1]} - {contact[2]} - {contact[3]} - {contact[4]}")

def on_select(event=None):
    selected_item = contacts_listbox.curselection()
    if selected_item:
        selected_contact = contacts_listbox.get(selected_item[0])
        contact_id = int(selected_contact.split(" - ")[0])
        return contact_id
    else:
        return None

def update_selected_contact():
    contact_id = on_select()
    if contact_id:
        update_contact(contact_id, name_entry.get(), phone_entry.get(), email_entry.get(), category_var.get())

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    category_var.set("")

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 10

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def change_theme(theme):
    if theme == "Dark":
        window.config(bg="black")
        contacts_listbox.config(bg="gray", fg="white")
        name_entry.config(bg="gray", fg="white")
        phone_entry.config(bg="gray", fg="white")
        email_entry.config(bg="gray", fg="white")
    else:
        window.config(bg="white")
        contacts_listbox.config(bg="white", fg="black")
        name_entry.config(bg="white", fg="black")
        phone_entry.config(bg="white", fg="black")
        email_entry.config(bg="white", fg="black")

def upload_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])
    if file_path:
        print(f"Photo uploaded: {file_path}")

if __name__ == "__main__":
    create_table()
    main()

