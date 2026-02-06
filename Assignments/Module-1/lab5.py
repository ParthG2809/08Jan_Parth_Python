#Practical Example 1: Write a Python program to print each fruit in a list using a simple for loop. List1 = ['apple', 'banana', 'mango']
List1 = ['apple', 'banana', 'mango']
for i in List1:
    print(i)

#Practical Example 2: Write a Python program to find the length of each string in List1
print("\n")
List1 = ['apple', 'banana', 'mango']
for i in List1:
    print(i, f"The length of string is {len(i)}")

#Practical Example 3: Write a Python program to find a specific string in the list using a simple for loop and if condition.
print("\n")
List1 = ['apple', 'banana', 'mango']
print(List1)
target_string = input("Enter the target string: ")

for i in List1:
    if i == target_string :
        print(f"The target string is found at index {List1.index(i)}: {target_string}")
        break
else:
    print("Item not in the list")

#Practical Example 4: Print this pattern using nested for loop: markdown Copy code * ** *** **** ***** 
print("\n")
for i in range(1, 6):
    for j in range(i):
        print("* ", end=" ")
    print(" ")