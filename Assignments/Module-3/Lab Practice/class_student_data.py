class studinfo:
    def __init__(self,id,name,city):
        self.id = id
        self.name = name
        self.city = city

stdata = []

no_of_students = int(input("Enter the number of students: "))
for i in range(no_of_students):
    id = int(input("Enter an ID: "))
    nm = input("Enter a Name: ")
    ct = input("Enter a City: ")

    st=studinfo(id, nm, ct)
    stdata.append(st)

student_data = []
for i in stdata:
    student_data.append([i.id, i.name, i.city])

print(student_data)