import keyword

x=keyword.kwlist
keyword_list = []
'''for i in x:
    print(f"The reserved keywords are: {i}")'''

for j in x:
    keyword_list.append(j)

print(keyword_list)