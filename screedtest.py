#!/usr/bin/python

from math import *
from random import *

black_count = 4
blue_count = 3
red_count = 4
acc_target = 1

def roll(color):
    rolly = ceil(random()*8)

    if color == "black":
        if rolly < 3: return (0)
        elif rolly < 7: return (1)
        else: return (2)

    elif color == "blue":
        if rolly < 3: return ("a")
        elif rolly < 7: return (1)
        else: return (1)

    elif color == "red":
        if rolly < 3: return (0)
        elif rolly <4: return ("a")
        elif rolly < 6: return (1)
        elif rolly < 8: return (1)
        else: return (2)


def screed(burnme,critmelist,critmeitem):
    del burnme
    if critmelist == "black":
        blacks[critmeitem] = 2
    elif critmelist == "blue":
        blues[critmeitem] = 1
    elif critmelist == "red":
        reds[critmeitem] = 1

blacks = []
blues = []
reds = []

for die in range(black_count):
    blacks.append(roll("black"))

for die in range(blue_count):
    blues.append(roll("blue"))

for die in range(red_count):
    reds.append(roll("red"))

print(blacks)
print(blues)
print(reds)

# count accuracies

accs = 0

for x in enumerate(blues+reds):
    print("Enumerating "+str(x))
    if x[1] == 'a':
        accs += 1


# OE

for x in enumerate(blacks):
    #~ print("Checking:",x[1])
    if x[1] < 2:
        #~ print("  Rerolling a "+str(x[1]))
        newroll = roll("black")
        #~ print("  New roll is a "+str(newroll))
        blacks[x[0]]=newroll

print("\n")
print("OE:  " + str(blacks))


# Screed

num_dice = len(blacks)

num_noncrits = 0
for x in blacks:
    if x < 2: num_noncrits += 1

if num_noncrits > 1:
    screedable = 0
    screeded = 0
    for x in enumerate(blacks):
        if (x[1] == 0 and not screedable and not screeded):
            print("Burning "+str(x))
            del blacks[x[0]]
            screedable = 1
        elif (x[1] == 0 and screedable and not screeded):
            print("Screeding "+str(x))
            blacks[x[0]] = 2
            screeded = 1
    if not screedable and not screeded:
        for x in enumerate(blacks):
            if (x[1] == 1 and not screedable and not screeded):
                print("Burning "+str(x))
                del blacks[x[0]]
                screedable = 1
            elif (x[1] == 1 and screedable and not screeded):
                print("Screeding "+str(x))
                blacks[x[0]] = 2
                screeded = 1

print("Screed:  " + str(blacks))
