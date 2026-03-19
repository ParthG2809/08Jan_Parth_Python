import tkinter
from tkinter import ttk, messagebox

x=tkinter.Tk()
x.title("MyApp")
x.geometry("400x500")
x.configure(bg="orange")

l1 = tkinter.Label(text="Firstname", bg="orange", fg="blue",font="Corbel 15 bold")
#l1.pack()
#l1.place(x=0, y=0)
l1.grid(row=0, column=0, sticky='w')

l2 = tkinter.Label(text="Lastname", bg="orange", fg="blue",font="Corbel 15 bold")
#l2.pack()
#l2.place(x=0, y=30)
l2.grid(row=1, column=0, sticky='w')

t1 = tkinter.Entry()
t1.grid(row=0, column=1, sticky='w')

t2 = tkinter.Entry()
t2.grid(row=1, column=1, sticky='w')

m=tkinter.Radiobutton(value=0, text="Male", bg="orange", fg="blue",font="Corbel 15 bold")
f=tkinter.Radiobutton(value=1, text="Female", bg="orange", fg="blue",font="Corbel 15 bold")

m.grid(row=2, column=0, sticky='w')
f.grid(row=2, column=1, sticky='w')

c1=tkinter.Checkbutton(text="Gujarati", bg="orange", fg="blue",font="Corbel 15 bold")
c2=tkinter.Checkbutton(text="Hindi", bg="orange", fg="blue",font="Corbel 15 bold")
c3=tkinter.Checkbutton(text="English", bg="orange", fg="blue",font="Corbel 15 bold")

c1.grid(row=3, column=0, sticky='w')
c2.grid(row=4, column=0, sticky='w')
c3.grid(row=5, column=0, sticky='w')

city = ["Rajkot", "Ahmedabad", "Gandhinagar", "Surat", "Baroda"]
cm = ttk.Combobox(x, values=city)
cm.grid(row=6, column=0, sticky='w')

def btnClick():
    print("Firstname: ", t1.get())
    print("Lastname: ", t2.get())

    messagebox.showinfo("Hello", f"Welcome {t1.get()}")

btn = tkinter.Button(text="Submit",fg="blue",font="Corbel 15 bold", command=btnClick)
btn.place(x=160, y=240)

x.mainloop()