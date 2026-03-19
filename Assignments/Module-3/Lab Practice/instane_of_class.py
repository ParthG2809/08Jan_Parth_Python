class student:
    stid = 102
    stname = "Parth"

    def getdata(self):
        print("ID:", self.stid)
        print("Name: ", self.stname)

st=student()    #object
st.getdata()
st.stid = 101
st.stname = "Parth"
st.getdata()

# Note: Object can access and modify the values of class
# Object allocates memory for all the functions, variables, modules of the class
# Object can be called outside of the same file

student().getdata()   #instance
student.stid = 103
student.stname = "Samarth"
student().getdata()

# Note: Instance can only access the values of class
# Instance allocates memory for only the method called
# Instance cannot be called outside of the same file