import pymysql

try:
    db=pymysql.connect(host='localhost', user='root', password='', database='testdb')
    print("Database connected")
except Exception as e:
    print(e)

cr = db.cursor()

#Table Create
tbl_create = "create table studinfo(id integer primary key auto_increment, name text, city text)" #use _ in auto increment for pymysql

try:
    cr.execute(tbl_create)
    print("Table created successfully!")
except Exception as e:
    print(e)

def insert_data():
    #Insert Data
    n = int(input("Enter the number of data you want to add: "))

    for i in range(n):
        nm = input("Enter your name: ")
        ct = input("Enter your city: ")
        insert_data = f"insert into studinfo(name, city) values ('{nm}', '{ct}')"
        cr.execute(insert_data)

    try:
        db.commit()
        print("Data inserted successfully!")
    except Exception as e:
        print(e)

def update_data():
    #Update data
    selection = input("What do you want to update? (name/city): ")

    id = int(input("Enter ID to update: "))

    if selection == "name":
        nm_update = input("Enter new name: ")
        update_data = f"update studinfo SET name = '{nm_update}' WHERE id = {id}"
        cr.execute(update_data)

    elif selection == "city":
        ct_update = input("Enter new city: ")
        update_data = f"update studinfo SET city = '{ct_update}' WHERE id = {id}"
        cr.execute(update_data)

    else:
        print("Invalid choice!")

    try:
        db.commit()
        print("Data updated successfully!")
    except Exception as e:
        print(e)

def delete_data():
    #Delete Data
    id = int(input("Enter ID to delete: "))

    delete_data = f"delete from studinfo where id = {id}"

    try:
        cr.execute(delete_data)
        db.commit()
        print("Data deleted Successfully!")
    except Exception as e:
        print(e)

def show_data():
    #Select Data
    select_data = "select * from studinfo"

    try:
        cr.execute(select_data)
        data = cr.fetchall()
        for i in data:
            print(i)

    except Exception as e:
        print(e)


while True:
    print("Menu for Databse Operation")
    print("1. Insert Data")
    print("2. Update Data")
    print("3. Delete Data")
    print("4. Show Data")
    print("5. Exit")

    choice = input("Enter your choice: ")

    #Insert Data
    if choice == "1":
        insert_data()

    #Update Data
    elif choice == "2":
        update_data()

    #Delete Data
    elif choice == "3":
        delete_data()

    #Select Data
    elif choice == "4":
        show_data()
        
    elif choice == "5":
        print("Exiting program")
        break

    else:
        print("Invalid choice!")