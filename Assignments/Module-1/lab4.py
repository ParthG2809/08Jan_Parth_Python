# Practical Example 5: Write a Python program to find greater and less than a number using if_else

number = int(input("Enter a number:"))
fix_number = int(input("Enter a comparison number:"))

if number > fix_number:
    print(f"{number} is greater than the comparison number {fix_number} ")
elif number < fix_number:
    print(f"{number} is less than the comparison number {fix_number} ")
else:
    print(f"{number} is equal to the comparison number {fix_number}")

# Practical Example 6: Write a Python program to check if a number is prime using if_else
print("\n")
number = int(input("Enter a number:"))

if number > 1:
    if number == 2:
        print("The number is Prime")
    elif number % 2 == 0:
        print("The number is Not Prime")
    else:
        print("The number is Prime")
else:
    print("The number is Not Prime")

# Practical Example 7: Write a Python program to calculate grades based on percentage using if-else ladder
print("\n")
percentage = float(input("Enter percentage:"))

if percentage >= 90:
    print("Grade: A")
elif percentage >= 75:
    print("Grade: B")
elif percentage >= 60:
    print("Grade: C")
elif percentage >= 40:
    print("Grade: D")
else:
    print("Grade: Fail")

# Practical Example 8: Write a Python program to check if a person is eligible to donate blood using a nested if. 
print("\n")
age = int(input("Enter age: "))
weight = int(input("Enter weight (in kg): "))

if age >= 18:
    if weight >= 50:
        print("You are eligible to donate blood")
    else:
        print("You are not eligible due to low weight")
else:
    print("You are not eligible due to age")
