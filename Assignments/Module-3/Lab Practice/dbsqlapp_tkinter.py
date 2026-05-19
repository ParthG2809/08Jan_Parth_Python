import tkinter as tk
from tkinter import messagebox
import pymysql

# ---------------- DB CONNECTION ---------------- #
try:
    db = pymysql.connect(host='localhost', user='root', password='', database='testdb')
    print("Database connected")
except Exception as e:
    print(e)

cr = db.cursor()

# ---------------- TABLE CREATE ---------------- #
tbl_create = """CREATE TABLE IF NOT EXISTS stdata(
id INT PRIMARY KEY AUTO_INCREMENT,
firstname TEXT,
lastname TEXT,
city TEXT)"""

cr.execute(tbl_create)

# ---------------- WINDOW ---------------- #
x = tk.Tk()
x.title("Database Application")
x.geometry("500x400")
x.config(bg='lightblue')

# ---------------- LABELS ---------------- #
tk.Label(x, text="ID:", bg='lightblue').grid(row=0, column=0, sticky='w')
tk.Label(x, text="First Name:", bg='lightblue').grid(row=1, column=0, sticky='w')
tk.Label(x, text="Last Name:", bg='lightblue').grid(row=2, column=0, sticky='w')
tk.Label(x, text="City:", bg='lightblue').grid(row=3, column=0, sticky='w')

# ---------------- ENTRY FIELDS ---------------- #
id_text = tk.Entry(x)
id_text.grid(row=0, column=1)

fnm_text = tk.Entry(x)
fnm_text.grid(row=1, column=1)

lnm_text = tk.Entry(x)
lnm_text.grid(row=2, column=1)

ct_text = tk.Entry(x)
ct_text.grid(row=3, column=1)

# Dropdown for update
choice_var = tk.StringVar()
choice_var.set("firstname")

tk.Label(x, text="Update Field:", bg='lightblue').place(x=300, y=20)
tk.OptionMenu(x, choice_var, "firstname", "lastname", "city").place(x=300, y=50)

# ---------------- FUNCTIONS ---------------- #

# INSERT
def insert_data():
    fnm = fnm_text.get()
    lnm = lnm_text.get()
    ct = ct_text.get()

    try:
        cr.execute(
            "INSERT INTO stdata(firstname, lastname, city) VALUES (%s, %s, %s)",
            (fnm, lnm, ct)
        )
        db.commit()

        # Get auto ID
        new_id = cr.lastrowid

        # Show ID
        id_text.delete(0, tk.END)
        id_text.insert(0, new_id)

        messagebox.showinfo("Success", f"Data Inserted! ID = {new_id}")

        # Clear fields
        fnm_text.delete(0, tk.END)
        lnm_text.delete(0, tk.END)
        ct_text.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# UPDATE
def update_data():
    id_val = id_text.get()
    choice = choice_var.get()

    try:
        if choice == "firstname":
            val = fnm_text.get()
            cr.execute("UPDATE stdata SET firstname=%s WHERE id=%s", (val, id_val))

        elif choice == "lastname":
            val = lnm_text.get()
            cr.execute("UPDATE stdata SET lastname=%s WHERE id=%s", (val, id_val))

        elif choice == "city":
            val = ct_text.get()
            cr.execute("UPDATE stdata SET city=%s WHERE id=%s", (val, id_val))

        db.commit()
        messagebox.showinfo("Success", "Data Updated!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# DELETE
def delete_data():
    id_val = id_text.get()

    try:
        cr.execute("DELETE FROM stdata WHERE id=%s", (id_val,))
        db.commit()
        messagebox.showinfo("Success", "Data Deleted!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# DISPLAY
def show_data():
    try:
        cr.execute("SELECT * FROM stdata")
        data = cr.fetchall()

        if not data:
            messagebox.showinfo("Data", "No records found")
            return

        result = ""
        for row in data:
            result += f"ID: {row[0]}, Name: {row[1]} {row[2]}, City: {row[3]}\n"

        messagebox.showinfo("All Records", result)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ---------------- BUTTONS ---------------- #
tk.Button(x, text="Insert", width=10, command=insert_data).place(x=20, y=150)
tk.Button(x, text="Update", width=10, command=update_data).place(x=120, y=150)
tk.Button(x, text="Delete", width=10, command=delete_data).place(x=220, y=150)
tk.Button(x, text="Display", width=10, command=show_data).place(x=320, y=150)

# ---------------- RUN ---------------- #
x.mainloop()