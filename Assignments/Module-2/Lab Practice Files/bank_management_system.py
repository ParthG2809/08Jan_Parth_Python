balance = 5000

def account():
    acc_no = int(input("Enter the account no: "))
    acc_name = input("Enter the account holder name: ")
    acc_type = input("Enter the account type: ")

    return acc_no, acc_name, acc_type

def deposit():
    global balance
    amount = int(input("\nEnter the amount to be deposited: "))
    if amount < 2000:
        print("Minimum 2000 is to be deposited")
    else:
        balance += amount
        print("Amount Deposited")
        print(f"The balance is {balance}")

def withdrawl():
    global balance
    withdraw = int(input("\nEnter the amount to be withdrawn: "))

    if withdraw > balance:
        print("Insufficient balance")
    else:
        balance = balance - withdraw
        print("Withdrawl possible")
        print(f"Remaining balance is {balance}")

def statement(acc_no, acc_name, acc_type, balance):
    print("\n\033[1mAccount Statement\033[0m")
    print("Account No: ", acc_no)
    print("Account Name: ", acc_name)
    print("Account Type: ", acc_type)
    print("Total Balance: ", balance)

acc_no, acc_name, acc_type = account()
deposit()
withdrawl()
statement(acc_no, acc_name, acc_type, balance)