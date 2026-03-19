# Practical Example 1: Write a Python program to create a database and a table using SQLite3.
import sqlite3

try:
    db = sqlite3.connect("studentinfo.db")
    print("Databse, created/connected!")
except Exception as e:
    print(e)

#Table create
tbl_create = "create table studinfo(id integer primary key autoincrement, name text, city text)"

try:
    db.execute(tbl_create)
    print("Table created successfully!")
except Exception as e:
    print(e)


# Practical Example 2: Write a Python program to insert data into an SQLite3 database and fetch it.
import sqlite3

db = sqlite3.connect("studentinfo.db")

#Insert data
insert_data = "insert into studinfo (name, city) values ('Parth', 'Rajkot'), ('Samarth', 'Ahmedabad'), ('Kunal', 'Hyderabad')"

try:
    db.execute(insert_data)
    db.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(e)

#Select data
select_data = "select * from studinfo"

try:
    db.execute(select_data)
    db.commit()
    print("Data Fetched Successfully!")
except Exception as e:
    print(e)