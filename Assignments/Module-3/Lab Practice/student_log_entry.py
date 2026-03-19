import datetime
fl = open("Student Log Entry.txt", "a")

n = int(input("Enter the number of Students: "))

for i in range(n):
    dt = datetime.datetime.now()
    stid = i+1
    stname = input("Enter the name: ")
    stcity = input("Enter the city: ")

    fl.write(f"Entry time: {dt}\nID: {stid}\nName: {stname}\nCity: {stcity}\n\n")
    i += i