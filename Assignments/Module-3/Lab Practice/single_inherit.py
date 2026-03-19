# Single Inheritance
class father:
    balance:int
    cars:int

    def getdata(self):
        self.balance = input("Enter the bank balance: ")
        self.cars = input("Enter the number of cars: ")

class son(father):
    def printdata(self):
        print("Bank balance:", self.balance)
        print("Number of Cars:", self.cars)

sn=son()
sn.getdata()
sn.printdata()