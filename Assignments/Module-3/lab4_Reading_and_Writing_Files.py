# Practical Example 1: Write a Python program to create a file and print the string into the file
file = open("data.txt", "w")

file.write("Python Programming\n")
file.write("File Handling Example\n")
file.write("Writing multiple lines into a file\n")

file.close()

print("Data written successfully.")

# Practical Example 2: Write a Python program to read a file and print the data on the console.
file = open("data.txt", "r")

content = file.read()

print("File contents are:")
print(content)

file.close()

# Practical Example 3: Write a Python program to check the current position of the file cursor using tell().
file = open("data.txt", "r")

print("Current position of cursor:", file.tell())

file.read(10)

print("Position after reading 10 characters:", file.tell())

file.close()