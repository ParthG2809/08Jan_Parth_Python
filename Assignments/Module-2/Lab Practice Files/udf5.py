def student_info(id, name, city, subjects):
    print("ID: ",id)
    print("Name: ",name)
    print("City: ",city)
    print("Subjects: ", subjects)
    print("Total marks: ", sum(subjects))

students = []
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    stid = int(input("Enter the student ID: "))
    stname = input("Enter the student name: ")
    stcity = input("Enter the student city: ")

    no_of_subjects = int(input("Enter the number of subjects: "))
    subjects = []

    for j in range(no_of_subjects):
        marks = int(input(f"Enter subject {j+1} marks: "))
        subjects.append(marks)

    student_info(stid, stname, stcity, subjects)
    students.append([stid, stname, stcity, subjects, sum(subjects)])

print(students)