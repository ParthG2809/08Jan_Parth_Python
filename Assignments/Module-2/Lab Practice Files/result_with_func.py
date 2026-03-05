def student_info(id, name, city, subjects):
    print("Id: ", id)
    print("Name: ", name)
    print("City: ", city)
    
    print("Subjects and Marks: ")
    total = 0
    for subject, marks in subjects.items():
        print(f"{subject} : {marks}")
        total += marks

    percentage = total / len(subjects)

    print("Total Marks: ", total)
    print("Percentage: ", percentage)

    return total, percentage

students = []
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    stid = int(input("Enter the student ID: "))
    stname = input("Enter the student name: ")
    stcity = input("Enter the student city: ")

    no_of_subjects = int(input("Enter the number of subjects: "))
    subjects = {}

    for j in range(no_of_subjects):
        subject_name = input(f"Enter subject {j+1} name: ")
        marks = int(input(f"Enter {subject_name} marks: "))
        subjects[subject_name] = marks

    total, percentage = student_info(stid, stname, stcity, subjects)
    students.append({
        "id": stid, 
        "name": stname, 
        "city": stcity, 
        "subjects": subjects,
        "total": total,
        "percentage": percentage
    })

print("\nSTUDENT RESULT TABLE")
print("-" * 75)
print(f"{'ID':^5} {'Name':^15} {'City':^15} {'Total':^10} {'Percentage':^10}")
print("-" * 75)

for student in students:
    print(f"{student['id']:^5} "
          f"{student['name']:^15} "
          f"{student['city']:^15} "
          f"{student['total']:^10} "
          f"{student['percentage']:^10.2f}")

print("-" * 75)
