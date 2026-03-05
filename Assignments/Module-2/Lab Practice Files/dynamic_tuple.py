'''city = ()
elements = int(input("Enter the number of elements of the tuple: "))

for i in range(elements):
    elements = input("Enter the city: ", )
    city = city + (elements,)

print(city)'''

city = []
elements = int(input("Enter the number of elements of the tuple: "))

for i in range(elements):
    data = input("Enter the city: ")
    city.append(data)

print(tuple(city))