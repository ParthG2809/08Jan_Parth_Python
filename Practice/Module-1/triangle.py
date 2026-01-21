a = int(input("Enter side 1: "))
b = int(input("Enter side 2: "))
c = int(input("Enter side 3: "))

if a+b>c and b+c>a and a+c>b:
    if a == b == c:
        print("Equilateral Traingle")
    elif a == b or b == c or a == c:
        print("Isosceles Traingle")
    else:
        print("Scalene Traingle")
else:
    print("Invalid Traingle")