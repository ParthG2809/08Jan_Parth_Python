class studinfo:
    __stid = 101        #Private    
    __stname = "Parth"  #Private

    def __getdata(self): #Private
        print("This is getdata")
        print("ID: ", self.__stid)
        print("Name: ", self.__stname)

    def printdata(self): #Public
        self.__getdata()

st=studinfo()
st.printdata()

# Note: Private is declared using __ before the variable name or function name. They cannot be used outside of the class