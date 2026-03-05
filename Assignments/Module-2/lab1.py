# Practical Example 1: Write a Python program to create a list with elements of multiple data types (integers, strings, floats, etc.). 
print("\033[1mPython program to create a list with elements of multiple data types (integers, strings, floats, etc.). \033[0m\n")
list = ["Parth", 12, 60.5436, True, [1, 2, 3]]
for i in list:
    print(type(i))

# Practical Example 2: Write a Python program to find the length of a list using the len() function.
print("\n\033[1mPython program to find the length of a list using the len() function. \033[0m\n")
name = "My name is Parth"
print(len(name))

# Practical Example 3: Write a Python program to access elements at different index positions. 
print("\n\033[1mPython program to access elements at different index positions. \033[0m\n")
data = [1234, "Parth", 3.14, False, [4, 5, 6]]
print("Element at index 0:", data[0])
print("Element at index 1:", data[1])
print("Element at index 2:", data[2])
print("Element at index 3:", data[3])
print("Element at index 4:", data[4])
print("Element at index -1 (last element):", data[-1])
print("Element at index -2:", data[-2])