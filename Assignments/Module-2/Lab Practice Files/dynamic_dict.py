student = {}
pairs = int(input("Enter the number of key-value pairs: "))

for i in range(pairs):
    key = input("Enter the key: ")
    value = input("Enter value: ")
    student[key] = value

print(student)