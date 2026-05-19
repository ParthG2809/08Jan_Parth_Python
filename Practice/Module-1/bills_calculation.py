# 1) Water Bill Calculation
units = int(input("Enter water units: "))
bill = 0

while units > 0:
    if units > 100:
        bill += (units - 100) * 8
        units = 100
    elif units > 50:
        bill += (units - 50) * 5
        units = 50
    else:
        bill += units * 3
        units = 0

print("Total Water Bill:", bill)

# 2) Mobile Data usage Bill
'''data = float(input("Enter data usage (GB): "))
bill = 0

while data > 0:
    if data <= 2:
        bill = 100
    elif data <= 5:
        bill = 200
    else:
        bill = 300
    break

print("Mobile Data Bill:", bill)'''

# 3) Parking Charges
'''hours = int(input("Enter parking hours: "))
charge = 0

while hours > 0:
    if hours > 5:
        charge += (hours - 5) * 50
        hours = 5
    elif hours > 2:
        charge += (hours - 2) * 40
        hours = 2
    else:
        charge += hours * 30
        hours = 0

print("Total Parking Charge:", charge)'''

# 4) Internet Plan Billing
'''usage = int(input("Enter monthly usage (GB): "))
bill = 0

while usage > 0:
    if usage <= 100:
        bill = 500
    elif usage <= 300:
        bill = 800
    else:
        bill = 1200
    break

print("Internet Bill:", bill)'''

# 5) Cab Fare Calculation
'''distance = int(input("Enter distance (km): "))
fare = 0

while distance > 0:
    if distance > 15:
        fare += (distance - 15) * 20
        distance = 15
    elif distance > 5:
        fare += (distance - 5) * 15
        distance = 5
    else:
        fare += distance * 10
        distance = 0

print("Total Cab Fare:", fare)'''

# 6) Gas Consumption Bill
'''units = int(input("Enter gas units: "))
bill = 0

while units > 0:
    if units > 50:
        bill += (units - 50) * 10
        units = 50
    elif units > 20:
        bill += (units - 20) * 8
        units = 20
    else:
        bill += units * 6
        units = 0

print("Total Gas Bill:", bill)'''

# 7) Courier Charges
'''weight = float(input("Enter weight (kg): "))
charge = 0

while weight > 0:
    if weight <= 1:
        charge = 50
    elif weight <= 5:
        charge = 100
    else:
        charge = 200
    break

print("Courier Charge:", charge)'''


# 8) Exan Fee Structure
'''subjects = int(input("Enter number of subjects: "))
fee = 0

while subjects > 0:
    if subjects <= 3:
        fee = 500
    elif subjects <= 6:
        fee = 900
    else:
        fee = 1200
    break

print("Total Exam Fee:", fee)'''


# 9) Toll Tax Calculation
'''vehicle = input("Enter vehicle type(bike/car/truck): ")
toll = 0

if vehicle == "bike" or vehicle == "car" or vehicle == "truck":
    distance = int(input("Enter the distance: "))

    if vehicle == "bike":
        toll = 2
    elif vehicle == "car":
        toll = 5
    elif vehicle == "truck":
        toll = 10

    print("Total toll is: ", toll * distance)

else:
    print("Invalid Vehicle")'''


# 10) Hotel Room Rent
'''days = int(input("Enter number of days: "))
rent = 0

while days > 0:
    if days > 5:
        rent += (days - 5) * 1200
        days = 5
    elif days > 2:
        rent += (days - 2) * 1500
        days = 2
    else:
        rent += days * 2000
        days = 0

print("Total Hotel Rent:", rent)
'''