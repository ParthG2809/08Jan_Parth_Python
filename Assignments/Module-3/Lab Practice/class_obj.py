class student:
    stid = 101
    stname = "Parth"

    def myfunc(self, a, b):
        print("Sum = ", a+b)

    def marks(self):
        sub1 = int(input("Enter marks of subject 1: "))
        sub2 = int(input("Enter marks of subject 2: "))
        print("Marks obtained in Subject 1: ",sub1)
        print("Marks obtained in Subject 2: ",sub2)

st=student()
print("ID:",st.stid)
print("Name:",st.stname)
st.myfunc(20,68)
st.marks()
