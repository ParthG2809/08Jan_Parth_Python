balance = 5000

try:
    amount = int(input("Enter the amount to be withdrawn: "))
    result = balance / amount
except ZeroDivisionError:
    print("You cannot enter 0")
except ValueError:
    print("Please enter a valid number")
else:
    if amount <= balance:
        balance -= amount
        print("Withdrawl successful")
        print("Remaining balance is ", balance)
    else:
        print("Insufficient balance")
finally:
    print("Thank you visiting the ATM") 