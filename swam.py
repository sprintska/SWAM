#!/usr/bin/python3.4
#!python

'''To run this script, make sure you have Python 3 installed, then type
py path/to/script/swam.py on the command line.  It was written and
tested for Python 3.4.  If you have Python 2, go get 3 and stop being a
weiner.  If you have a newer version, hello from the distant past!

This is a Monte Carlo simulation script built to model expected damage 
profiles in Star Wars Armada.  It's pretty rudimentary.  If you don't 
know Python, you should only change the variables under OPTIONS.  To add
the effect of an upgrade, set the variable equal to 1; to remove it, set
it to 0. The color_base variables set the number of dice in the pool.


The die number-to-facing translation I'm using is:

BLACK
1-2     Blank
3-6     Hit
7-8     Hit/Crit

BLUE
1-2     Accuracy
3-6     Hit
7-8     Crit

RED
1-2     Blank
3       Accuracy
4-5     Hit
6-7     Crit
8       Double
'''

from random import *
from math import *
import os
import sys

configs = {}

#####OPTIONS (Set to 1 for yes, 0 for no)#####

configs["conf_file"]=False         # use a config file
configs["tries"]=100000            # how many iterations to try
configs["distance"]=0              # Range: 0 for close, 1 for medium, 2 for long
configs["black_base"]=0            # number of black dice (base)
configs["blue_base"]=0             # number of blue dice (base)
configs["red_base"]=0              # number of red dice (base)
configs["acm"]=0                   # ACM available?
configs["apt"]=0                   # APT available?
configs["ackbar"]=0                # Ackbar available?
configs["cf"]=0                    # concentrate fire available?
configs["leading_shots"]=0         # LS available?
configs["oe"]=0                    # OE available?
configs["salvation"]=0			   # Salvation available?
configs["trc"]=0                   # TRC available?
configs["vader"]=0                 # Vader available?
configs["dist_override_black"]=0   # Distance override for blacks (e.g., Defiant)
configs["dist_override_blue"]=0    # Distance override for blues (e.g., Defiant)

##############################################

def soDumb():
    print("Try swam.py --help for help.")
    exit()

def accept_args(args_list,import_configs):
    for arg in enumerate(args_list):
        #~ arg=(arg[0],arg[1].lower())
        #~ print(arg)
        if ("--help" in str(arg[1])) or (str(arg[1])=="-h"):
            print("SWAM - Star Wars Armada Modeler")
            print("Last update: 13 Feb 2016\n")
            print("Usage: swam.py [option=value]")
            print("       swam.py --config filename (not implemented)\n")
            print("Options:")
            print("  -h  --help          Help text")
            print("  -c  --config        Use options in a config file\n")
            print("  -i  --iter          Number of iterations")
            print("  -r  --range         Range to target (close|medium|long)\n")
            print("  -ba --blacks        Number of black dice")
            print("  -bu --blues         Number of blue dice")
            print("  -re --reds          Number of red dice\n")
            print("  -ab --ackbar        Admiral Ackbar")
            print("  -ac --acm           Assault Concussion Missiles")
            print("  -ap --apt           Assault Proton Torpedoes")
            print("  -cf --cf            Concentrate Fire")
            print("  -ls --ls            Leading Shots")
            print("  -oe --oe            Ordnance Experts")
            print("  -tr --trc           Turbolaser Reroute Circuits")
            print("  -va --vader         Vader (Admiral)\n")
            print("  -ao --black_override   Distance override for blacks")
            print("  -uo --blue_override    Distance override for blues\n\n")  
            print("Example: swam.py --config ./mc30.swm")
            print("         swam.py --iter=1000 --range=long --reds=3")
            print("         swam.py -i 1000 -r long -ba 3 -bl 2 -ab -ac")

        elif "--iter" in str(arg[1]):
            try: import_configs["tries"]=\
                 int((str(arg[1]).split("=",1))[1])
            except: soDumb()
                
        elif "--range" in str(arg[1]):
            try: import_configs["distance"]=\
                 int((str(arg[1]).split("=",1))[1])
            except: soDumb()
                
        elif "--blacks" in str(arg[1]):
            try: import_configs["black_base"]=int((str(arg[1]).split("=",1))[1])
            except: soDumb()
                
        elif "--blues" in str(arg[1]):
            try: import_configs["blue_base"]=\
                 int((str(arg[1]).split("=",1))[1])
            except: soDumb()
            
        elif "--reds" in str(arg[1]):
            try: import_configs["red_base"]=\
                 int((str(arg[1]).split("=",1))[1])
            except: soDumb
            
        elif str(arg[1]) == "--ackbar": import_configs["ackbar"]=1
        elif str(arg[1]) == "--acm": import_configs["acm"]=1
        elif str(arg[1]) == "--apt": import_configs["apt"]=1
        elif str(arg[1]) == "--cf": import_configs["cf"]=1
        elif str(arg[1]) == "--ls": import_configs["leading_shots"]=1
        elif str(arg[1]) == "--oe": import_configs["oe"]=1
        elif str(arg[1]) == "--salvation": import_configs["salvation"]=1
        elif str(arg[1]) == "--trc": import_configs["trc"]=1
        elif str(arg[1]) == "--vader": import_configs["vader"]=1
        elif str(arg[1]) == "--black_override": import_configs["dist_override_black"]=1
        elif str(arg[1]) == "--blue_override": import_configs["dist_override_blue"]=1
        
    return import_configs

# Read in arguments from command line

configs = accept_args(sys.argv,configs)
#~ print("Foo: ",configs)

conf_file=configs["conf_file"]
tries=configs["tries"]
distance=configs["distance"]
black_base=configs["black_base"]
blue_base=configs["blue_base"]
red_base=configs["red_base"]
acm=configs["acm"]
apt=configs["apt"]
ackbar=configs["ackbar"]
cf=configs["cf"]
leading_shots=configs["leading_shots"]
oe=configs["oe"]
salvation=configs["salvation"]
trc=configs["trc"]
vader=configs["vader"]
dist_override_black=configs["dist_override_black"]
dist_override_blue=configs["dist_override_blue"]

# Initialize some variables
damage_overall=0        # Total damage
accuracies_overall=0    # How many times we got at least 1 acc
fails_overall=0         # How many times we failed to get a black crit
if ackbar and red_base: red_base += 2   # Ackbar hurrrr

# Pretty text
print("Rolling "+str(black_base)+" blacks, "
                +str(blue_base)+" blues, and "
                +str(red_base)+" reds, "
                +str(tries)+" times.")
print("Factors in play:")
if cf: print("    Concentrate Fire")
if trc: print("    Turbolaser Reroute Circuits")
if acm: print("    ACM")
if apt: print("    APT")
if ackbar: print("    Ackbar")
if oe: print("    Ordnance Experts")
if salvation: print("    Salvation")
if vader: print("    Vader")
if leading_shots: print("    Leading Shots")
if distance==0: print("\nAt close range\n===============\n")
if distance==1: print("\nAt medium range\n===============\n")
if distance==2: print("\nAt long range\n===============\n")

# Iteration Loop

for x in range(tries):
    
#Reset
    crit=0
    accuracy=0
    cf_spent=0
    damage=0
    fails=0
    accuracies=0
    if trc: trc_available=1
    else: trc_available=0

#initial dice pool
    
    blacks=[]
    if distance==0 or dist_override_black:
        for die in range(black_base):
            blacks.append(ceil(random()*8))
    
    blues=[]
    if distance<=1 or dist_override_blue:
        for die in range(blue_base):
            blues.append(ceil(random()*8))
    
    reds=[]
    for die in range(red_base):
        reds.append(ceil(random()*8))

    
###BLACKS###
#CF if available and fishing for an APT/ACM crit
    if (acm or apt):    
        for x in blacks:
            if x > 6: crit=1

        if cf and not crit:
            blacks.append(ceil(random()*8))
            cf_spent=1


#OE reroll logic

    if oe:
        for x in blacks:
            if x > 6: crit=1

        if (acm or apt) and not crit:
            for black in enumerate(blacks):
                blacks[black[0]]=ceil(random()*8)

        else:
            for black in enumerate(blacks):
                if black[1] < 3:
                    blacks[black[0]]=ceil(random()*8)

#Black damage total

    for x in blacks:
        if x > 6: crit=1
    
    if not crit:
        fails+=1

    for die in blacks:
        if die > 6: damage += 2
        elif die > 2: damage += 1


###BLUES###

#Check reds and blues for accuracies
    for die in blues:
        if die < 3: 
            accuracy=1
            accuracies+=1
    for die in reds:
        if die==3: 
            accuracy=1
            accuracies+=1

#CF to fish for an acc if none
    if cf and not cf_spent and not accuracy:
        blues.append(ceil(random()*8))

    for die in blues:
        if die > 2: damage += 1
        else: 
            accuracy=1
            accuracies+=1

###REDS###
    
    #Vader

    #If we don't have LS, reroll more conservatively
    if vader and not leading_shots:
        for red in enumerate(reds):
            if red[1] <= 2: 
                reds[red[0]]=ceil(random()*8)
            elif (red[1] == 3) and not accuracy:
                accuracy = 1
            elif (red[1] == 3) and accuracy:    # Reroll acc if 2+ accs
                reds[red[0]]=ceil(random()*8)   # are showing           

    #If we have LS, fish for doubles
    elif vader and leading_shots and blues:
        for red in enumerate(reds):
            if (red[1] != 3) and (red[1] != 8): 
                reds[red[0]]=ceil(random()*8)
            elif (red[1] == 3) and not accuracy:
                accuracy = 1
            elif (red[1] == 3) and accuracy:
                reds[red[0]]=ceil(random()*8)

    #TRC
    if trc_available:
        
        #look for a blank to reroll
        for red in enumerate(reds):
            if trc_available and (red[1] < 3):
                reds[red[0]]=8
                trc_available=0
        
        #look for a single to reroll
        for red in enumerate(reds):
            if (red[1] > 3) and (red[1] < 8) and trc_available:
                reds[red[0]]=8
                trc_available=0
        
        #look for an acc to reroll if there is another one showing AND
        #the the total showing damage is 1 or less
        dmg_showing = 0
        for die in blacks:
            if die > 6: dmg_showing += 2
            elif die > 2: dmg_showing += 1
        for blue in blues:
            if die > 2: dmg_showing += 1
        for red in reds:
            if die == 8: dmg_showing += 2
            elif die > 3: dmg_showing += 1
        for red in enumerate(reds):
            if (red[1] == 3) and \
               ((accuracies > 1) or \
               (dmg_showing <= 2)) and \
               trc_available:
                reds[red[0]]=8
                trc_available=0
                accuracies-=1 
    
    #Count damage
    for die in reds:
        if die > 7: damage += 2
        elif (die > 5) and salvation: damage += 2
        elif die > 3: damage += 1
        elif die == 3: accuracy=1

###THE REST OF CF###
    if (len(reds) > 0) and trc_available and crit and cf and not cf_spent:
        reds.append(2)
        damage += 2
        cf_spent = 1
    
    elif cf and not cf_spent:
        cf_black = ceil(random()*8)
        if cf_black < 3:
            cf_black = ceil(random()*8)
            
        if cf_black > 6: 
            crit = 1
            damage += 2
        if cf_black > 2: damage += 1
        blacks.append(cf_black)
        

    if acm and crit: damage += 2
    if apt and crit: damage += 1

    accuracies_overall+=accuracy
    damage_overall+=damage
    fails_overall+=fails

    if tries==1:
        print("Blacks:",blacks,"\nBlues:",blues,"\nReds:",reds)

if (acm or apt):
    print(str(tries-fails_overall)+" black crits of "+str(tries)+" tries. \n"+
          str((tries-fails_overall)/tries)+" ACM/APT success rate.")
          
print(str(damage_overall/tries)+" average damage.")
print(str(round(100*accuracies_overall/tries,2))+"% chance of natural accuracy.")
