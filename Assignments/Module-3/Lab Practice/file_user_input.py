fl = open("new1.txt", "a")

'''stid = int(input("Enter the ID: "))
stname = input("Enter the name: ")

fl.write(f"ID is {stid}\nName is {stname}\n")'''

#For multiple user input
n = int(input("Enter the no of students"))
for i in range(n):
    stid = int(input("Enter the ID: "))
    stname = input("Enter the name: ")

    fl.write(f"ID is {stid}\nName is {stname}\n")