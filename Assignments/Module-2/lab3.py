# Practical Example 1: Write a Python program to iterate through a list and print each element
list = ["Parth", 12, 60.5436, True, [1, 2, 3]]

for i in list:
    print(i)

# Practical Example 2:  Write a Python program to insert elements into an empty list using a for loop and append(). 
numbers = []
for i in range(1, 6):
    numbers.append(i)

print(numbers)

# OR
students = []
number = int(input("Enter the number of students in the list: "))

for i in range(number):
    name = input("Enter the name: ")
    students.append(name)

print(students)