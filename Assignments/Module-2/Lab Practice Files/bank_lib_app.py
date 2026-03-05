from bank_lib import *

balance = 5000

acc_no, acc_name, acc_type = account()

while True:
    print("\n\033[1m----- MENU -----\033[0m")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Statement")
    print("4. Exit")

    choice = input("\nSelect an option: ")

    if choice == "1":
        balance = deposit(balance)

    elif choice == "2":
        balance = withdrawl(balance)

    elif choice == "3":
        statement(acc_no, acc_name, acc_type, balance)
        print("\n\033[1mHave a great day!\033[0m\n")
        break

    elif choice == "4":
        print("\033[1mHave a great day!\033[0m\n")
        break

    else:
        print("Invalid option. Try again.")
