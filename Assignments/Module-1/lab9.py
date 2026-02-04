# Practical Example 1: Write a Python program to demonstrate string slicing.
str = "Basics of Python"
print(str)
print(str[0])
print(str[1:5])
print(str[:8])
print(str[5:])
print(str[-1])
print(str[1:16:2])
print(str[::-1])
print(str[:])

# Practical Example 2: Write a Python program that manipulates and prints strings using various string methods.
str = "Welcome to Python"
print(str)
print("Uppercase:", str.upper())
print("Lowercase: ", str.lower())
print("Capitalize: ", str.capitalize())
print("Title: ", str.title())
print("Replace: ", str.replace("Python", "Programming"))
print("Index: ", str.index("Python"))
print("Count: ", str.count("o"))
print("Alphabetics: ", str.isalpha())
print("AlphaNumeric: ", str.isalnum())
print("Starts with: ", str.startswith("Welcome"))
print("Ends with: ", str.endswith("Python"))