# Practical Example 1: Write a Python program to show single inheritance.
class Parent:
    def show(self):
        print("This is the parent class")

class Child(Parent):
    def display(self):
        print("This is the child class")

c = Child()

c.show()
c.display()

# Practical Example 2: Write a Python program to show multilevel inheritance.
class Grandparent:
    def show1(self):
        print("This is the grandparent class")

class Parent(Grandparent):
    def show2(self):
        print("This is the parent class")

class Child(Parent):
    def show3(self):
        print("This is the child class")

c = Child()

c.show1()
c.show2()
c.show3()

# Practical Example 3: Write a Python program to show multiple inheritance.
class Father:
    def show_father(self):
        print("This is the father class")

class Mother:
    def show_mother(self):
        print("This is the mother class")

class Child(Father, Mother):
    def show_child(self):
        print("This is the child class")

c = Child()

c.show_father()
c.show_mother()
c.show_child()

# Practical Example 4: Write a Python program to show hierarchical inheritance.
class Parent:
    def show(self):
        print("This is the parent class")

class Child1(Parent):
    def display1(self):
        print("This is child1 class")

class Child2(Parent):
    def display2(self):
        print("This is child2 class")

c1 = Child1()
c2 = Child2()

c1.show()
c1.display1()

c2.show()
c2.display2()

# Practical Example 5: Write a Python program to show hybrid inheritance.
class A:
    def showA(self):
        print("Class A")

class B(A):
    def showB(self):
        print("Class B")

class C(A):
    def showC(self):
        print("Class C")

class D(B, C):
    def showD(self):
        print("Class D")

d = D()

d.showA()
d.showB()
d.showC()
d.showD()

# Practical Example 6: Write a Python program to demonstrate the use of super() in inheritance. 
class Parent:
    def show(self):
        print("This is the parent method")

class Child(Parent):
    def show(self):
        super().show()
        print("This is the child method")

c = Child()
c.show()