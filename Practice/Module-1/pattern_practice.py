#Right Angle Triangle * Pattern
'''rows = int(input("Enter the row size for the pattern: "))
for i in range(1, rows + 1):  # Outer loop for rows
    for j in range(1, i + 1):  # Inner loop for columns
        print("*", end=" ")   # Print star
    print()'''

#Reverse Right Angle Triangle * Pattern
'''rows = int(input("Enter the number of rows for the pattern: "))
for i in range(rows, 0, -1):
    for j in range(1, i + 1):
        print("* ", end=" ")
    print(" ")'''

#Pyramid Pattern
'''rows = int(input("Enter the number of rows: "))
for i in range(1, rows + 1):  # Outer loop for rows
    for j in range(rows  - i):  # Inner loop for spaces
        print(" ", end=" ")
    for k in range(1, 2 * i):  # Inner loop for stars
        print("*", end=" ")
    print(" ")'''

#Inverted Pyramid
'''rows = int(input("Enter the number of rows: "))
for i in range(rows, 0, -1):
    for j in range(rows - i):
        print(" ", end=" ")
    for k in range(1, 2*i):
        print("*", end=" ")
    print(" ")
'''
#Diamond Pattern
rows = int(input("Enter the number of rows: "))
for i in range(1, rows + 1):  # Outer loop for rows
    for j in range(rows  - i):  # Inner loop for spaces
        print(" ", end=" ")
    for k in range(1, 2 * i):  # Inner loop for stars
        print("*", end=" ")
    print(" ")
for i in range(rows-1, 0, -1):
    for j in range(rows - i):
        print(" ", end=" ")
    for k in range(1, 2*i):
        print("*", end=" ")
    print(" ")
