def student_info(id, name, city):
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

print(students)