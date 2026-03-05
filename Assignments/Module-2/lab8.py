# Practical Example 1:  Write a Python program to print a string using a function
def string_print():
    print("Hello welcome to functions in Python")

string_print()

# Practical Example 2:  Write a Python program to create a parameterized function that takes two arguments and prints their sum.
def getsum(a,b):
    print(f"The sum of {a} and {b} = {a+b}")

num1 = int(input("Enter the 1st number: "))
num2 = int(input("Enter the 2nd number: "))

getsum(num1, num2)

# Practical Example 3: Write a Python program to create a lambda function with one expression
square = lambda x: x * x

number = int(input("Enter a number: "))
print(f"The square of {number} is: {square(number)}")

# Practical Example 4:  Write a Python program to create a lambda function with two expressions.
sum = lambda a, b: a + b

num1 = int(input("Enter the 1st number: "))
num2 = int(input("Enter the 2nd number: "))
print(f"The sum of {num1} and {num2} is: {sum(num1, num2)}")