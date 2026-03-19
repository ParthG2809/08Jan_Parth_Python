class studinfo:
    stid:int
    stname:str
    sub1:str
    sub2:str
    sub1_marks:int
    sub2_marks:int

    def getdata(self):
        self.stid = input("Enter ID: ")
        self.stname = input("Enter name: ")
        self.sub1 = input("Enter subject 1 name: ")
        self.sub1_marks = input(f"Enter marks of {self.sub1}: ")
        self.sub2 = input("Enter Subject 2 name: ")
        self.sub2_marks = input(f"Enter marks of {self.sub2}: ")

    def printdata(self):
        print("ID: ",self.stid)
        print("Name: ",self.stname)
        print(f"Marks of {self.sub1}: {self.sub1_marks}")
        print(f"Marks of {self.sub2}: {self.sub2_marks}")

st=studinfo()
st.getdata()
st.printdata()