# Practical Example 1: Write a Python program to convert a list into a tuple.
list = ["Parth", 10, 20, 40, 60.82, True]
tuple = tuple(list)

print(f"List: {list}")
print(f"List converted to tuple: {tuple}")

# Practical Example 2: Write a Python program to create a tuple with multiple data types.
multi_data_tuple = ("Python", 20, False, 30.65)
print(f"Multiple Data Types Tuple: {multi_data_tuple}")

# Practical Example 3: Write a Python program to concatenate two tuples into one.
tuple1 = ("Python", "PHP", "Java")
tuple2 = ("HTML", "CSS", "JavaScript")

tuple3 = tuple1 + tuple2
print(f"Result tuple: {tuple3}")

# Practical Example 4: Write a Python program to access the value of the first index in a tuple
fruits = ("apple", "banana", "orange", "cherry")
print(f"Value of data at First Index: {fruits[0]}")