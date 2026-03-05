def student_info(id, name, city, marks):
    print("ID: ",id)
    print("Name: ",name)
    print("City: ",city)
    print("Marks: ",marks)

stid = int(input("Enter the student ID: "))
stname = input("Enter the student name: ")
stcity = input("Enter the student city: ")
stmarks = int(input("Enter the student marks: "))

student_info(stid, stname, stcity, stmarks)