# Practical Example 1: Write a Python program to show method overloading.
class Calculator:

    def add(self, a, b=0, c=0):
        result = a + b + c
        print("Sum:", result)

c = Calculator()

c.add(5, 3)
c.add(5, 3, 2)

# Practical Example 2: Write a Python program to show method overriding. 
class Parent:

    def show(self):
        print("This is the parent class method")

class Child(Parent):

    def show(self):
        print("This is the child class method")

c = Child()
c.show()