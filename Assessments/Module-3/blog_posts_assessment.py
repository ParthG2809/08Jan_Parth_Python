import tkinter
from tkinter import ttk, messagebox
import os

x = tkinter.Tk()
x.title("MiniBlog")
x.geometry("500x500")
x.configure(bg="SlateBlue4")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("Blog.TButton", font="Corbel 12 bold", padding=10)

# Labels
l1 = tkinter.Label(text="Enter Name:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l1.grid(row=0, column=0, sticky='w')

l2 = tkinter.Label(text="Post Title:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l2.grid(row=1, column=0, sticky='w')

l3 = tkinter.Label(text="Post Content:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l3.grid(row=2, column=0, sticky='w')

# Entry fields
t1 = tkinter.Entry()
t1.grid(row=0, column=1)

t2 = tkinter.Entry()
t2.grid(row=1, column=1)

content = tkinter.Text(height=5, width=30)
content.grid(row=2, column=1)

# Listbox
l4 = tkinter.Label(text="Saved Posts:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l4.place(x=10, y=200)

post_list = tkinter.Listbox(width=25)
post_list.place(x=10, y=230)

# Display area
l5 = tkinter.Label(text="Post Content:", bg="SlateBlue4", fg="white", font="Corbel 12 bold")
l5.place(x=250, y=200)

display = tkinter.Text(height=10, width=25)
display.place(x=250, y=230)

# Create folder
if not os.path.exists("posts"):
    os.makedirs("posts")

# Save Post
def save_post():
    name = t1.get()
    title = t2.get()
    text = content.get("1.0", tkinter.END).strip()

    if name == "" or title == "" or text == "":
        messagebox.showerror("Error", "All fields are required")
        return

    filename = f"posts/{name}_{title}.txt"

    try:
        file = open(filename, "a")
        file.write(text)
        file.close()

        print("Post Saved:", filename)
        messagebox.showinfo("Success", "Post saved successfully")

        load_posts()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Load Posts
def load_posts():
    post_list.delete(0, tkinter.END)

    files = os.listdir("posts")

    for f in files:
        post_list.insert(tkinter.END, f)

# View Post
def view_post(event):
    try:
        selected = post_list.get(post_list.curselection())

        file = open("posts/" + selected, "r")
        data = file.read()
        file.close()

        print("Post Content:\n", data)

        display.delete("1.0", tkinter.END)
        display.insert(tkinter.END, data)

    except:
        messagebox.showerror("Error", "File not found")

post_list.bind("<<ListboxSelect>>", view_post)

# Buttons (styled like your calculator)
btn1 = ttk.Button(text="Save Post", style="Blog.TButton", command=save_post)
btn1.place(x=150, y=150)

btn2 = ttk.Button(text="Load Posts", style="Blog.TButton", command=load_posts)
btn2.place(x=300, y=150)

x.mainloop()