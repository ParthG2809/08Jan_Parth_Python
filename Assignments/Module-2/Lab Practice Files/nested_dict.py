students = {}
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    students[f"Student {i+1}"] = {
        "id": int(input("Enter the id: ")),
        "name": input("Enter the name: "),
        "city": input("Enter the city: ")
    }

print(students)

# Method 2: Using append
'''students = []
no_of_students = int(input("Enter the number of students: "))

for i in range(no_of_students):
    students.append({
        "id": int(input("Enter the id: ")),
        "name": input("Enter the name: "),
        "city": input("Enter the city: ")
    })

print(students)'''