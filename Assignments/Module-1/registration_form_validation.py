firstname = input("Enter your First name: ")
lastname = input("Enter your Last name: ")
email = input("Enter your email: ")
mobile = input("Enter your mobile number: ")
password = input("Enter your password: ")
cpass = input("Confirm your password: ")

if firstname.isalpha():
    print(firstname)
else:
    print("Invalid First name")

if lastname.isalpha():
    print(lastname)
else:
    print("Invalid Last name")

if email.islower():
    print(email)
else:
    print("Invalid Email")

if mobile.isdigit() and len(mobile)==10:
    print(mobile)
else:
    print("Invalid mobile number")

if len(password) >= 8 and len(password) <= 12:
    print(password)
else:
    print("Invalid Password")

if cpass == password:
    print(cpass)
else:
    print("Passwords are different. Please enter the Password again.")