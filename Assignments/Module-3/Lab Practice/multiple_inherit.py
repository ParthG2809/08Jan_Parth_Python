# Multiple Inheritance
class father:
    balance:int
    cars:int

    def getdata(self):
        self.balance = input("Enter the bank balance: ")
        self.cars = input("Enter the number of cars: ")

class mother():
    property:int
    def getdata2(self):
        self.property = input("Enter the no of properties: ")

class son(father, mother):
    def printdata(self):
        print("Bank balance:", self.balance)
        print("Number of Cars:", self.cars)
        print("No of properties: ",self.property)

sn=son()
sn.getdata()
sn.getdata2()
sn.printdata()