# Practical Example 1: Practical Examples: Write a Python program to create a class and access the properties of the class using an object.
class Student:
    name = "Parth"
    age = 25

s1 = Student()

print("Name:", s1.name)
print("Age:", s1.age)

# Practical Example 2: Write a Python program to demonstrate the use of local and global variables in a class.
x = 50   # Global variable

class Demo:

    def show(self):
        y = 20   # Local variable
        print("Local variable:", y)
        print("Global variable:", x)

d = Demo()
d.show()