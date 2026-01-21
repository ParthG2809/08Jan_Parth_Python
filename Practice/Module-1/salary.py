basic = float(input("Enter basic salary: "))

if basic <= 10000:
    hra = basic * 0.2
    da = basic * 0.8
elif basic <= 20000:
    hra = basic * 0.25
    da = basic * 0.9
else:
    hra = basic * 0.3
    da = basic * 0.95

pf = basic * 0.12
gross = basic + hra + da - pf

print("Net Salary:", gross)
