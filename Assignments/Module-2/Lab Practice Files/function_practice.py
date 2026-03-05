'''def greeting(name="User"):
    print("Hello", name)

print(greeting("Parth"))'''

def student_info(id, name, city):
    return{
        "name": name,
        "city": city
    }

students = {}
no_of_students = int(input("Enter the no of students: "))

for i in range(no_of_students):
    stid = int(input("Enter the student id: "))
    stname = input("Enter the student name: ")
    stcity = input("Enter the student city: ")

    students[f"Student Id: {stid}"] = student_info(stid,stname, stcity)

print(students)