# Practice Example 1: Write a generator function that generates the first 10 even numbers. 
def even_numbers():
    num = 2
    count = 0
    while count < 10:
        yield num
        num += 2
        count += 1

# Using the generator
for i in even_numbers():
    print(i)

# Practical Example 2: Write a Python program that uses a custom iterator to iterate over a list of integers. 
class ListIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

# Using the custom iterator
numbers = [10, 20, 30, 40, 50]
obj = ListIterator(numbers)

for num in obj:
    print(num)

