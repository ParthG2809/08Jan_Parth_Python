class students:
    def getdata(self, stid, stname):
        print("ID: ", stid)
        print("Name: ",stname)

st=students()
stdid = int(input("Enter student id: "))
stdname = input("Enter student name: ")
st.getdata(stdid, stdname)