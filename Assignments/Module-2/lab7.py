# Practical Example 1: Write a Python program to update a value at a particular key in a dictionary.
data = {
    "id": 101,
    "name": "Parth",
    "city": "Rajkot"
}

print(data)

data["city"] = "Ahmedabad"
print(f"Updated Dictionary: {data}")

# Practical Example 2: Write a Python program to separate keys and values from a dictionary using keys() and values() methods.
print("\n")
student = {
    "id": 101,
    "name": "Parth",
    "city": "Rajkot"
}

print(f"Keys: {student.keys()}")
print(f"Values: {student.values()}")

# Practical Example 3: Write a Python program to convert two lists into one dictionary using a for loop.
print("\n")
keys = ["id", "name", "technology", "city"]
values = [101, "Parth", "Python", "Rajkot"]
result = {}

for i in range(len(keys)):
    result[keys[i]] = values[i]

print(result)

# Practical Example 4: Write a Python program to count how many times each character appears in a string.
text = input("Enter a string: ")

count_dict = {}

for ch in text:
    if ch in count_dict:
        count_dict[ch] += 1
    else:
        count_dict[ch] = 1

print("Character Count:")
for key, value in count_dict.items():
    print(key, ":", value)
