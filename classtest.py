#!/usr/bin/python3

class Foo(object):
    def __init__(self,name):
        self.name = name
        self.food = 0
        
    def giveFood(self,new_food=3):
        self.food += new_food
        
    def eatFood(self,hungriness=4):
        self.food -= hungriness
        
Cory = Foo("Cory")

print(Cory.food)

Cory.giveFood(7)

print(Cory.food)

Cory.eatFood(2)

print(Cory.food)