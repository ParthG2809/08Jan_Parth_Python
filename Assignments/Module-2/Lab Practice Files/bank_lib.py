def account():
    acc_no = int(input("Enter the account no: "))
    acc_name = input("Enter the account holder name: ")
    while True:
        acc_type = input("Enter account type (savings/current): ").lower()

        if acc_type in ("savings", "current"):
            acc_type = acc_type.capitalize()
            break
        else:
            print("Invalid account type! Please enter only 'savings' or 'current'.")
    return acc_no, acc_name, acc_type


def deposit(balance):
    amount = int(input("\nEnter the amount to be deposited: "))
    if amount < 2000:
        print("Minimum 2000 is to be deposited")
    else:
        balance += amount
        print("Amount Deposited")
        print(f"The balance is {balance}")
    return balance


def withdrawl(balance):
    withdraw = int(input("\nEnter the amount to be withdrawn: "))
    if withdraw > balance:
        print("Insufficient balance")
    else:
        balance -= withdraw
        print("Withdrawal successful")
        print(f"Remaining balance is {balance}")
    return balance


def statement(acc_no, acc_name, acc_type, balance):
    print("\n\033[1m----------Account Statement----------\033[0m")
    print("Account No:", acc_no)
    print("Account Name:", acc_name)
    print("Account Type:", acc_type, "Account")
    print("Total Balance:", balance)
    print("\033[1m-------------------------------------\033[0m")
