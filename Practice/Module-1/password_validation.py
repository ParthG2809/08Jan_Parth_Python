password = "admin@123"
attempts = 0

while attempts < 3:
    user = input("Enter password: ")
    if user == password:
        print("Login Successful")
        break
    attempts += 1

else:
    print("Too many tries. Account blocked")