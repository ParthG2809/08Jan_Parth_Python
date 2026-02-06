# Practical Example 1: Apply map() to square a list of numbers
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x * x, numbers))

print(squares)

# Practical Example 2: Use reduce() to find the product of a list of numbers
from functools import reduce

numbers = [1, 2, 3, 4, 5]
product = reduce(lambda x, y: x * y, numbers)

print(product)

# Practical Example 3: Filter out even numbers using filter()
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

print(even_numbers)