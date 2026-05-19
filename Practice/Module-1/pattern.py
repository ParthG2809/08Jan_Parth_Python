'''n = 5
for i in range(1, n + 1):
    for j in range(i):
        print("*", end=" ")
    print()'''

'''n = 5
for i in range(n, 0,-1):
    for j in range(1, i+1):
        print("*", end=" ")
    print()'''

'''n = 5
for i in range(1, n + 1):  # Outer loop for rows
    for j in range(n  - i):  # Inner loop for spaces
        print(" ", end=" ")
    for k in range(1, 2 * i):  # Inner loop for stars
        print("*", end=" ")
    print()'''

'''n = 5
for i in range(n, 0, -1):  # Outer loop for rows
    for j in range(n - i):  # Inner loop for spaces
        print(" ", end=" ")
    for k in range(1, 2 * i):  # Inner loop for stars
        print("*", end=" ")
    print()'''