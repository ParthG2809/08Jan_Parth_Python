import sqlite3

try:
    db = sqlite3.connect("personal_info.db")
    print("Database created/connected successfully!")
except Exception as e:
    print(e)

#Table create
table_create = "create table information(id integer primary key autoincrement, name text, city text)"

try:
    db.execute(table_create)
    db.commit()
    print("Table created successfully!")
except Exception as e:
    print(e)

#Insert data
n = int(input("Enter the number of data you want to add: "))

for i in range(n):
    nm = input("Enter your name: ")
    ct = input("Enter your city: ")
    insert_data = f"insert into information(name, city) values ('{nm}', '{ct}')"
    db.execute(insert_data)

try:
    db.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(e)

#Update data
choice = input("What do you want to update? (name/city): ")

id = int(input("Enter ID to update: "))

if choice == "name":
    nm_update = input("Enter new name: ")
    update_data = f"UPDATE information SET name = '{nm_update}' WHERE id = {id}"
    db.execute(update_data)

elif choice == "city":
    ct_update = input("Enter new city: ")
    update_data = f"UPDATE information SET city = '{ct_update}' WHERE id = {id}"
    db.execute(update_data)

else:
    print("Invalid choice!")

try:
    db.commit()
    print("Data updated successfully!")
except Exception as e:
    print(e)

#Delete Data
id = int(input("Enter ID to delete: "))

delete_data = f"delete from information where id = {id}"

try:
    db.execute(delete_data)
    db.commit()
    print("Data deleted Successfully!")
except Exception as e:
    print(e)