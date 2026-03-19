import sqlite3

try:
    db=sqlite3.connect("topsdb.db")
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

#Insert data
insert_data = "insert into studinfo (name, city) values ('Parth', 'Rajkot'), ('Samarth', 'Ahmedabad'), ('Kunal', 'Hyderabad')"

try:
    db.execute(insert_data)
    db.commit()
    print("Data inserted successfully!")
except Exception as e:
    print(e)

#Update data
update_data = "update studinfo set city = 'Mumbai' where id = 3"

try:
    db.execute(update_data)
    db.commit()
    print("Data Update Successfully!")
except Exception as e:
    print(e)

#Delete data
delete_data = "delete from studinfo where id in (4, 5, 6)"

try:
    db.execute(delete_data)
    db.commit()
    print("Data deleted Successfully!")
except Exception as e:
    print(e)