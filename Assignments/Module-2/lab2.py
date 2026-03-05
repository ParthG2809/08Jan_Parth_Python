# Practical Example 1: Write a Python program to update a list using insert() and append().
print("\033[1mPython program to update a list using insert() and append().\033[0m\n")
numbers = [10, 20, 30]
print(numbers)

numbers.append(40)
print("Updated List using append():", numbers)

numbers.insert(1, 15)
print("Updated List using insert():", numbers)

# Practical Example 2: Write a Python program to remove elements from a list using pop() and remove()
print("\n\033[1mPython program to remove elements from a list using pop() and remove()\033[0m\n")
fruits = ["apple", "banana", "cherry", "mango"]
print("Original List:", fruits)

fruits.pop(1)
print("List after removal using pop():", fruits)


fruits.remove("cherry")
print("List after removal using remove():", fruits)

