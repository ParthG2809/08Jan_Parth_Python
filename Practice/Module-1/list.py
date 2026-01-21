'''fruits = input("Enter elements for the list: ").split()
print("List of fruits is:", fruits)'''

a = []
n = int(input("Enter the number of elements: "))
for i in range(n):
    element = input(f"Enter element {i+1}: ")
    a.append(element)

print("List:", a)
sentence = " ".join(a)
print(sentence)