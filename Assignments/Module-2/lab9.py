# Practical Example 1:  Write a Python program to demonstrate the use of functions from the math module.
import math

num = float(input("Enter a number: "))

print("Square Root:", math.sqrt(num))
print("Power (num^2):", math.pow(num, 2))
print("Ceiling Value:", math.ceil(num))
print("Floor Value:", math.floor(num))
print("Factorial (only for integers):", math.factorial(int(num)))

# Practical Example 2:  Write a Python program to generate random numbers between 1 and 100 using the random module.
import random

# Direct method
print(f"Random number between 1 and 100: {random.randint(1, 100)}")

# Stored in Variable
num = random.randint(1, 100)
print("Random number between 1 and 100:", num)

# To print more than 1 random integers
for i in range(5):
    print(f"5 random intergers are: {random.randint(1, 100)}")