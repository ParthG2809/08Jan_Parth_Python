import tkinter
from tkinter import ttk

x = tkinter.Tk()
x.title("Calculator")
x.geometry("400x500")
x.configure(bg="SlateBlue4")

style = ttk.Style()
style.theme_use("clam")

style.configure("Calc.TButton", font="Corbel 12 bold", padding=10)

l1 = tkinter.Label(text="Enter First number:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l1.grid(row=0, column=0, sticky='w')

l2 = tkinter.Label(text="Enter Second number:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l2.grid(row=1, column=0, sticky='w')

t1 = tkinter.Entry()
t1.grid(row=0, column=1)

t2 = tkinter.Entry()
t2.grid(row=1, column=1)

output = tkinter.Label(text="Result:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
output.grid(row=2, column=0)

def add():
    a = float(t1.get())
    b = float(t2.get())
    result = a + b
    output.config(text="Result: " + str(result))
    print("Addition:", result)

def multiply():
    a = float(t1.get())
    b = float(t2.get())
    result = a * b
    output.config(text="Result: " + str(result))
    print("Multiply:", result)

def divide():
    a = float(t1.get())
    b = float(t2.get())
    result = a / b
    output.config(text="Result: " + str(result))
    print("Division:", result)

def subtract():
    a = float(t1.get())
    b = float(t2.get())
    result = a - b
    output.config(text="Result: " + str(result))
    print("Subtraction:", result)

btn1 = ttk.Button(text="+", style="Calc.TButton", command=add)
btn1.place(x=10, y=150)

btn2 = ttk.Button(text="*", style="Calc.TButton", command=multiply)
btn2.place(x=100, y=150)

btn3 = ttk.Button(text="/", style="Calc.TButton", command=divide)
btn3.place(x=190, y=150)

btn4 = ttk.Button(text="-", style="Calc.TButton", command=subtract)
btn4.place(x=280, y=150)

x.mainloop()