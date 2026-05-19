import pymysql

try:
    db=pymysql.connect(host="localhost", user="root", password="", database="newtestdb")
    print("Database Connected")
except Exception as e:
    print(e)

