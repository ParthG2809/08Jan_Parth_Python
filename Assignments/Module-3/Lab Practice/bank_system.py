import random

class account:
    balance:int
    def __init__(self):
        self.acc_no = random.randint(1000000, 9999999)
        self.balance = 8000

    def getdata(self):
        self.acc_holder = input("Enter the account holder name: ")
        #self.acc_type = input("Enter whether the account is a Savings Account or Current Account: ")
        while True:
            acc_type = input("Enter account type (savings/current): ").lower()

            if acc_type in ("savings", "current"):
                self.acc_type = acc_type.capitalize()
                break
            else:
                print("Invalid account type! Please enter only 'savings' or 'current'.")

class deposit(account):
    def depositdata(self):
        amount = int(input("Enter the amount to be deposited: "))

        if amount < 2000:
            print("Minimum 2000 is to be deposited")
            print(f"The balance is {self.balance}")
        else:
            self.balance += amount
            print("Amount Deposited")
            print(f"The new balance is {self.balance}")
    
class withdrawl(deposit):

    def withdrawldata(self):
        withdrawl = int(input("Enter the amount to be withdrawn: "))

        if withdrawl > self.balance:
            print("Insufficient balance")
            print(f"The balance remains the same i.e. {self.balance}")
        else:
            self.balance -= withdrawl
            print("Withdrawal successful")
            print(f"Remaining balance is {self.balance}")
    
class statement(withdrawl):
    def printdata(self):
        print("\n\033[1m----------------------------------------\033[0m")
        print("\033[1mAccount Statement\033[0m")
        print("Account no: ",self.acc_no)
        print("Account Holder Name: ", self.acc_holder)
        print("Account Type(Savings/Current): ",self.acc_type)
        print("Final balance: ",self.balance)
        print("\033[1m----------------------------------------\033[0m")

st=statement()
st.getdata()
st.depositdata()
st.withdrawldata()
st.printdata()