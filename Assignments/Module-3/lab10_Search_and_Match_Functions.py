# Practical Example 1: Write a Python program to search for a word in a string using re.search().
import re

text = "Python programming is easy"

result = re.search("programming", text)

if result:
    print("Word found in the string")
else:
    print("Word not found")

# Practical Example 2: Write a Python program to match a word in a string using re.match(). 
import re

text = "Python programming"

result = re.match("Python", text)

if result:
    print("Word matched at the beginning of the string")
else:
    print("No match found")