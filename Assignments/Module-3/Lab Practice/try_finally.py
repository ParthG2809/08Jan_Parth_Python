try:
    num1 = int(input("Enter A: "))
    num2 = int(input("Enter B: "))
    print("Sum = ", num1+num2)
except ValueError as v:
    print(v)
finally:
    print("This is the finally block")