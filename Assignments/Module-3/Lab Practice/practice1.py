import tkinter
from tkinter import messagebox

x = tkinter.Tk()
x.title("Calculator")
x.geometry("400x300")
x.configure(bg="orange")

# Labels
l1 = tkinter.Label(text="Enter First Number", bg="orange", fg="blue", font="Corbel 15 bold")
l1.grid(row=0, column=0, sticky='w')

l2 = tkinter.Label(text="Enter Second Number", bg="orange", fg="blue", font="Corbel 15 bold")
l2.grid(row=1, column=0, sticky='w')

# Entry boxes
t1 = tkinter.Entry()
t1.grid(row=0, column=1, sticky='w')

t2 = tkinter.Entry()
t2.grid(row=1, column=1, sticky='w')

# Result Label
result_label = tkinter.Label(text="Result:", bg="orange", fg="blue", font="Corbel 15 bold")
result_label.grid(row=6, column=0, columnspan=2)

# Functions
def add():
    a = float(t1.get())
    b = float(t2.get())
    result = a + b
    print("Addition:", result)
    result_label.config(text="Result: " + str(result))

def subtract():
    a = float(t1.get())
    b = float(t2.get())
    result = a - b
    print("Subtraction:", result)
    result_label.config(text="Result: " + str(result))

def multiply():
    a = float(t1.get())
    b = float(t2.get())
    result = a * b
    print("Multiplication:", result)
    result_label.config(text="Result: " + str(result))

def divide():
    try:
        a = float(t1.get())
        b = float(t2.get())
        result = a / b
        print("Division:", result)
        result_label.config(text="Result: " + str(result))
    except ZeroDivisionError:
        messagebox.showerror("Error", "Cannot divide by zero")

# Buttons
b1 = tkinter.Button(text="Add", fg="blue", font="Corbel 12 bold", command=add)
b1.grid(row=3, column=0)

b2 = tkinter.Button(text="Subtract", fg="blue", font="Corbel 12 bold", command=subtract)
b2.grid(row=3, column=1)

b3 = tkinter.Button(text="Multiply", fg="blue", font="Corbel 12 bold", command=multiply)
b3.grid(row=4, column=0)

b4 = tkinter.Button(text="Divide", fg="blue", font="Corbel 12 bold", command=divide)
b4.grid(row=4, column=1)

x.mainloop()