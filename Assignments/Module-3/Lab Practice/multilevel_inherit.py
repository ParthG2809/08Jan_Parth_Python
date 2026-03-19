# Multilevel Inheritance
class father:
    balance:int
    cars:int
    properties:int

    def getdata(self):
        self.balance = input("Enter the bank balance: ")
        self.cars = input("Enter the number of cars: ")
        self.properties = input("Enter the no of properties: ")

class son1(father):
    def printdata(self):
        print("No of properties: ", self.properties)
    

class son2(son1):
    def printdata2(self):
        print("Bank balance:", self.balance)
        print("Number of Cars:", self.cars)

sn=son2()
sn.getdata()
sn.printdata2()
sn.printdata()