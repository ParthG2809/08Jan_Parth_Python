import re

username = input("Enter a name: ")

regex1 = re.findall(r'^[A-Za-z0-9]+$', username)
print(regex1)

if regex1:
    print("Match found")
else:
    print("Error")

email = input("Enter your email id: ")

regex2 = re.findall(r'[a-zA-Z0-9]+@[a-z]+\.[a-zA-Z]{2,}', email)
print(regex2)

if regex2:
    print("Match found")
else:
    print("Error") 