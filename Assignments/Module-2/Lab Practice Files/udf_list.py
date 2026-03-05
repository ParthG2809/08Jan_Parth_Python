'''def student_info(id, name, city):
    print("ID: ",id)
    print("Name: ",name)
    print("City: ",city)

students = []
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    stid = int(input("Enter the student ID: "))
    stname = input("Enter the student name: ")
    stcity = input("Enter the student city: ")

    student_info(stid, stname, stcity)
    students.append([stid, stname, stcity])

print(students)'''

# List of dictionaris
'''def student_info(id, name, city):
    print("ID: ",id)
    print("Name: ",name)
    print("City: ",city)

students = []
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    stid = int(input("Enter the student ID: "))
    stname = input("Enter the student name: ")
    stcity = input("Enter the student city: ")

    student_info(stid, stname, stcity)
    students.append({
        "id": stid,
        "name": stname,
        "city": stcity
    })

print(students)'''

# Dictionaries of list
def student_info(id, name, city):
    print("ID:", id)
    print("Name:", name)
    print("City:", city)

students = {}   # dictionary instead of list
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    stid = int(input("Enter the student ID: "))
    stname = input("Enter the student name: ")
    stcity = input("Enter the student city: ")

    student_info(stid, stname, stcity)

    students[f"Student {stid}"] = {
        stname,
        stcity
    }

print(students)

