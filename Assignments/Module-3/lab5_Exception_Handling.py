# Practical Example 1: Write a Python program to handle exceptions in a calculator.
try:
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    print("Select operation: +, -, *, /")
    op = input("Enter operator: ")

    if op == "+":
        print("Result:", a + b)

    elif op == "-":
        print("Result:", a - b)

    elif op == "*":
        print("Result:", a * b)

    elif op == "/":
        print("Result:", a / b)

    else:
        print("Invalid operator")

except ZeroDivisionError:
    print("Error: Cannot divide by zero")

except ValueError:
    print("Error: Invalid input")

# Practical Example 2: Write a Python program to handle multiple exceptions (e.g., file not found, division by zero).
try:
    file = open("data.txt", "r")
    print(file.read())

    num = int(input("Enter a number: "))
    result = 10 / num
    print("Result:", result)

except FileNotFoundError:
    print("Error: File not found")

except ZeroDivisionError:
    print("Error: Division by zero")

except ValueError:
    print("Error: Invalid input")

finally:
    print("Program executed")

# Practical Example 3: Write a Python program to handle file exceptions and use the finally block for closing the file.
try:
    file = open("data.txt", "r")
    content = file.read()
    print(content)

except FileNotFoundError:
    print("File does not exist")

finally:
    try:
        file.close()
        print("File closed successfully")
    except:
        print("File was not opened")

# Practical Example 4: Write a Python program to print custom exceptions.
try:
    age = int(input("Enter your age: "))

    if age < 0:
        raise ValueError("Age cannot be negative")

    print("Your age is:", age)

except ValueError as e:
    print("Custom Exception:", e)