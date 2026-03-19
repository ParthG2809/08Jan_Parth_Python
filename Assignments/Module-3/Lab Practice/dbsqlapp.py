import pymysql

try:
    db=pymysql.connect(host='localhost', user='root', password='', database='testdb')
    print("Database connected")
except Exception as e:
    print(e)

cr = db.cursor()

#Table create
tbl_create = "create table studinfo(id integer primary key auto_increment, name text, city text)" #use _ in auto increment for pymysql

try:
    cr.execute(tbl_create)
    print("Table created successfully!")
except Exception as e:
    print(e)