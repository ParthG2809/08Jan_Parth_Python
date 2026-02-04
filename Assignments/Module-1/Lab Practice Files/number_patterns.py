'''for i in range(1, 6):
    for j in range(1, i+1):
        print(j, end=" ")
    print(" ")'''


'''for i in range(1, 6):
    for j in range(i):
        print(i, end=" ")
    print(" ")'''

'''for i in range(1, 6):
    for j in range(i):
        print(chr(65+j), end=" ")
    print(" ")'''

#Pattern 1-15
'''n=1
for i in range(1, 6):
    for j in range(i):
        print(n, end=" ")
        n+=1
    print(" ")'''

#Reverse pattern 1-15
n=15
for i in range(5, 0, -1):
    for j in range(i):
        print(n, end=" ")
        n-=1
    print(" ")