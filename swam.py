#!/usr/bin/python3

'''To run this script, make sure you have Python 3 installed, then type
py path/to/script/swam.py on the command line.  It was written and
tested for Python 3.4.  If you have Python 2, go get 3 and stop being a
weiner.  If you have a newer version, hello from the distant past!

This is a Monte Carlo simulation script built to model expected damage
profiles in Star Wars Armada.  It's pretty rudimentary.  If you don't
know Python, you should only change the variables under OPTIONS.  To add
the effect of an upgrade, set the variable equal to 1; to remove it, set
it to 0.  The color_base variables set the number of dice in the pool.


The die number-to-facing convention I'm using is:

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
from collections import *
import os
import sys

configs = {}                        # dictionary for tying CL args or eventual
                                    # config file args to in-script variables

#####OPTIONS (Set to 1 for yes, 0 for no)#####

configs["conf_file"]=False          # use a config file
configs["tries"]=100000             # how many iterations to try
configs["showbrace"]=0             # show average braced damage
configs["acc_target"]=1             # how many accuracies to shoot for per shot
configs["distance"]=0               # range: 0 for close, 1 for medium, 2 for long
configs["black_base"]=0             # number of black dice (base)
configs["blue_base"]=0              # number of blue dice (base)
configs["red_base"]=0               # number of red dice (base)
configs["acm"]=0                    # ACM?
configs["apt"]=0                    # APT?
configs["ackbar"]=0                 # Ackbar?
configs["cf"]=0                     # Concentrate fire?
configs["leading_shots"]=0          # LS?
configs["oe"]=0                     # OE?
configs["salvation"]=0              # Salvation?
configs["screed"]=0                 # Screed?
configs["sensor"]=0                 # Sensor Teams?
configs["h9"]=0                     # H9s?
configs["trc"]=0                    # TRC?
configs["vader"]=0                  # Vader?
configs["dist_override_black"]=0    # Distance override for blacks (e.g., Defiance)
configs["dist_override_blue"]=0     # Distance override for blues (e.g., Defiance)

###############################################

class attackPool(object):
    """The current attack pool.
    """
    
    def __init__(self, reds=0, blues=0, blacks=0):
        pass

def soDumb():
    print("Try swam.py --help for help.")
    exit()
    
def helpText():
    print("Usage: swam.py [option=value]")
    print("       swam.py --config filename (not implemented)\n")
    print("Options:")
    print("  -h  --help          Help test")
    print("  -c  --config        Use options in a config file\n")
    print("  -i  --iter          Number of iterations")
    print("  -r  --range         Range to target (close|medium|long)\n")
    print("  -at --accuracies    Target number of accuracies on each shot\n")
    print("  -ba --blacks        Number of black dice")
    print("  -bu --blues         Number of blue dice")
    print("  -re --reds          Number of red dice")
    print("  -br --brace         Show average braced damage (does not account for acc)")
    print("  -ab --ackbar        Admiral Ackbar")
    print("  -ac --acm           Assault Concussion Missiles")
    print("  -ap --apt           Assault Proton Torpedoes")
    print("  -cf --cf            Concentrate Fire")
    print("  -ls --ls            Leading Shots")
    print("  -oe --oe            Ordnance Experts")
    print("  -sc --screed        Admiral Screed")
    print("  -st --sensor        Sensor Team")
    print("  -h9 --h9            H9 Turbolasers")
    print("  -tr --trc           Turbolaser Reroute Circuits")
    print("  -va --vader         Vader (Admiral)\n")
    print("  -ao --black_override   Distance override for blacks")
    print("  -uo --blue_override    Distance override for blues\n\n")
    print("Example: swam.py --config ./mc30.swm")
    print("         swam.py --iter=1000 --range=long --reds=3")
    print("         swam.py -i 1000 -r long -ba 3 -bl 2 -ab -ac")
    print("\n\nSWAM - Star Wars Armada Modeler")
    print("Last update: 19 March 2017\n")
    print("Written by: Ardaedhel")
    exit()
    
    
def accept_args(args_list,import_configs):
    for arg in enumerate(args_list):
        if ("--help" in str(arg[1])) or (str(arg[1])=="-h"):
            helpText()
            
        elif "--iter" in str(arg[1]):
            try: import_configs["tries"]=\
                int((str(arg[1]).split("=",1))[1])
            except: soDumb()
        elif "-i" == str(arg[1]):
            try: import_configs["tries"]=\
                int(str(args_list[arg[0]+1]))
            except: soDumb()
            
        elif "--accuracies" in str(arg[1]):
            try: import_configs["acc_target"]=\
                int((str(arg[1]).split("=",1))[1])
            except: soDumb()
        elif "-at" == str(arg[1]):
            try: import_configs["acc_target"]=\
                int(str(args_list[arg[0]+1]))
            except: soDumb()
            
        elif "--iter" in str(arg[1]):
            try: import_configs["tries"]=\
                int((str(arg[1]).split("=",1))[1])
            except: soDumb()
        elif "-i" == str(arg[1]):
            try: import_configs["tries"]=\
                int(str(args_list[arg[0]+1]))
            except: soDumb()
            
        elif "--range" in str(arg[1]):
            try: 
                if str(arg[1]).split("=",1) == "close":
                    import_configs["distance"]=0
                elif str(arg[1]).split("=",1) == "medium":
                    import_configs["distance"]=1
                elif str(arg[1]).split("=",1) == "long":
                    import_configs["distance"]=2
            except: soDumb()
        elif "-r" == str(arg[1]):
            try: 
                if str(args_list[arg[0]+1]) == "close":
                    import_configs["distance"]=0
                elif str(args_list[arg[0]+1]) == "medium":
                    import_configs["distance"]=1
                elif str(args_list[arg[0]+1]) == "long":
                    import_configs["distance"]=2
            except: soDumb()
            
        elif "--blacks" in str(arg[1]):
            try: import_configs["black_base"]=\
                int((str(arg[1]).split("=",1))[1])
            except: soDumb()
        elif "-ba" == str(arg[1]):
            try: import_configs["black_base"]=\
                int(str(args_list[arg[0]+1]))
            except: soDumb()
            
        elif "--blues" in str(arg[1]):
            try: import_configs["blue_base"]=\
                int((str(arg[1]).split("=",1))[1])
            except: soDumb()
        elif "-bu" == str(arg[1]):
            try: import_configs["blue_base"]=\
                int(str(args_list[arg[0]+1]))
            except: soDumb()
            
        elif "--reds" in str(arg[1]):
            try: import_configs["red_base"]=\
                int((str(arg[1]).split("=",1))[1])
            except: soDumb()
        elif "-re" == str(arg[1]):
            try: import_configs["red_base"]=\
                int(str(args_list[arg[0]+1]))
            except: soDumb()
            
        '''
        binary (yes or no) options:
        this list ties all command line flags (item[0]) to their
        associated variable
        '''
        
        nonbinary_options = [
            ("--ackbar","ackbar"),
            ("-ab","ackbar"),
            ("--acm","acm"),
            ("-ac","acm"),
            ("--apt","apt"),
            ("-ap","apt"),
            ("--cf","cf"),
            ("-cf","cf"),
            ("--ls","leading_shots"),
            ("-ls","leading_shots"),
            ("--oe","oe"),
            ("-oe","oe"),
            ("--screed","screed"),
            ("-sc","screed"),
            ("-h9","h9"),
            ("--h9","h9"),
            ("--sensor","sensor"),
            ("-st","sensor"),
            ("--trc","trc"),
            ("-tr","trc"),
            ("--salvation","salvation"),
            ("-sa","salvation"),
            ("--brace","showbrace"),
            ("-br","showbrace"),
            ("--vader","vader"),
            ("-va","vader"),
            ("--black_override","dist_override_black"),
            ("-ao","dist_override_black"),
            ("--blue_override","dist_override_blue"),
            ("-ue","dist_override_blue")
            ]
            
        for args_set in nonbinary_options:
            if str(arg[1]) == str(args_set[0]): import_configs[str(args_set[1])]=1
            
    return import_configs

def roll(color):
    '''Rolls a die of a given color, returns a string...
        * blank
        * hit
        * acc
        * crit
        * hitcrit
        * doublehit
        '''
    result = ceil(random()*8)
    if color.lower() == "black":
        if result < 3:
            return "blank"
        elif result < 7:
            return "hit"
        else: return "hitcrit"
    elif color.lower() == "blue":
        if result < 3:
            return "acc"
        elif result < 7:
            return "hit"
        else: return "crit"
    elif color.lower() == "red":
        if result < 3:
            return "blank"
        elif result < 4:
            return "acc"
        elif result < 6:
            return "hit"
        elif result < 8:
            return "crit"
        else: return "doublehit"
    
# Read in arguments from command line

configs = accept_args(sys.argv,configs)

acc_target=configs["acc_target"]
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
screed=configs["screed"]
sensor=configs["sensor"]
showbrace=configs["showbrace"]
h9=configs["h9"]
trc=configs["trc"]
vader=configs["vader"]
dist_override_black=configs["dist_override_black"]
dist_override_blue=configs["dist_override_blue"]

# Initialize some variables
damage_overall=0        # Total damage
braced_damage_overall=0 # Total damage if the target braced (not counting acc)
accuracies_overall=0    # How many times we got at least [target] accs
fails_overall=0         # How many times we failed to get a black crit
cr90s_killed=0          # How many times we've one-shotted a CR90
raiders_killed=0        # How many times we've one-shotted a Raider

if ackbar and red_base: red_base += 2   # Ackbar hurr

#Pretty text
print("Rolling "+str(black_base)+" blacks, "
                +str(blue_base)+" blues, and "
                +str(red_base)+" reds, "
                +str(tries)+" times.")
print("Factors in play:")
if cf: print("    Concentrate Fire")
if trc: print("    Turbolaser Reroute Circuits")
if acm: print("    ACM")
if apt: print("    APT")
if ackbar: print("    Admiral Ackbar")
if oe: print("    Ordnance Experts")
if salvation: print("    Salvation")
if screed: print("    Admiral Screed")
if sensor: print("    Sensor Teams")
if h9: print("    H9 Turbolasers")
if vader: print("    Darth Vader (Admiral)")
if leading_shots: print("    Leading Shots")
if distance==0: print("\nAt close range\n===================\n")
if distance==1: print("\nAt medium range\n===================\n")
if distance==2: print("\nAt long range\n===================\n")

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
    
        # roll aggressively if we have Vader as a backup
        if vader:
            for black in enumerate(blacks):
                if black[1] < 7:
                    blacks[black[0]]=ceil(random()*8)
                    
        # roll aggressively if we have Screed and enough dice to burn
        elif (screed and (len(blacks) + len(blues) + len(reds) >1)):
            for black in enumerate(blacks):
                if black[1] < 7:
                    blacks[black[0]]=ceil(random()*8)
                    
        else:
            for x in blacks:
                if x > 6: crit=1

            # roll aggressively if we have to fish for crits                
            if (acm or apt) and not crit:
                for black in enumerate(blacks):
                    blacks[black[0]]=ceil(random()*8)
                    
            else:
                for black in enumerate(blacks):
                    if black[1] < 3:
                        blacks[black[0]]=ceil(random()*8)

        
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
            
    #CF to fish for an acc if not enough
    if cf and not cf_spent and (accuracies < acc_target):
        blues.append(ceil(random()*8))

            
    ###REDS###

    #Vader
    
    #If we don't have LS, reroll more conservatively
    if vader and not leading_shots:
        for red in enumerate(reds):
            if red[1] <= 2:
                reds[red[0]]=ceil(random()*8)
            elif (red[1] == 3) and (accuracies < acc_target):
                accuracy = 1
            elif (red[1] == 3) and (accuracies >= acc_target):  # Reroll acc if
                reds[red[0]]=ceil(random()*8)                   # more showing
                accuracies-=1                                   # than wanted
                
    #If we have LS, fish for doubles
    elif vader and leading_shots and blues:
        for red in enumerate(reds):
            if (red[1] != 3) and (red[1] != 8):
                reds[red[0]]=ceil(random()*8)
            elif (red[1] == 3) and (accuracies < acc_target):
                accuracy = 1
            elif (red[1] == 3) and (accuracies >= acc_target):
                reds[red[0]]=ceil(random()*8)
                accuracies -= 1
    
    #LS
    if leading_shots:
        if (accuracies - acc_target) > 0:
            blanks = accuracies - acc_target
        else: blanks = 0
        
        for die in reds:
            if die < 4:
                blanks += 1
        
        crit = 0
        for die in blacks:
            if die < 3:
                blanks += 1
            if die > 6:
                crit = 1
                    
        if ((blanks >= 2) or ((apt or acm) and not crit)):
            ls_burned = 0
            if accuracies > acc_target:
                for die in enumerate(blues):
                    if ((not ls_burned) and (die[1] < 3)):
                        ls_burned = 1
                        del blues[die[0]]
                        accuracies -= 1
            else:
                for die in enumerate(blues):
                    if ((not ls_burned) and (die[1] < 7)):
                        ls_burned = 1
                        del blues[die[0]]
            if not ls_burned and blues:
                del blues[0]
                ls_burned = 1
            
            if ls_burned:
                for die in enumerate(blues):
                    if ((accuracies > acc_target) and (die[1] < 3)):
                        blues[die[0]] = ceil(random()*8)
                        accuracies -= 1

                for die in enumerate(reds):
                    if die[1] < 3:
                        reds[die[0]] = ceil(random()*8)
                    elif ((die[1] == 3) and (accuracies > acc_target)):
                        reds[die[0]] = ceil(random()*8)
                        accuracies -= 1

                if (acm or apt) and not crit:
                    for black in enumerate(blacks):
                        blacks[black[0]]=ceil(random()*8)
                        
                else:
                    for black in enumerate(blacks):
                        if black[1] < 3:
                            blacks[black[0]]=ceil(random()*8)
    
    #TRC
    if trc_available:
    
        #look for a blank to flip
        for red in enumerate(reds):
            if trc_available and (red[1] < 3):
                reds[red[0]]=8
                trc_available=0
                
        #look for a single to reroll
        for red in enumerate(reds):
            if (red[1] > 3) and (red[1] < 8) and trc_available:
                reds[red[0]]=8
                trc_available=0
                
        #look for an acc to reroll if there is another one showing OR
        #the total showing damage is 1 or less
        dmg_showing = 0
        for die in blacks:
            if die > 6: dmg_showing += 2
            elif die > 2: dmg_showing += 1
        for die in blues:
            if die > 2: dmg_showing += 1
        for die in reds:
            if die == 8: dmg_showing += 2
            elif die > 3: dmg_showing += 1
        for die in enumerate(reds):
            if (die[1] == 3) and ((accuracies > acc_target) or (dmg_showing <= 2)) and trc_available:
                reds[die[0]]=8
                trc_available=0
                accuracies-=1
    
                        
    #Check for black crits
    crit=0
                
    #Check for blue accs
    for die in blues:
        if die <= 2: 
            accuracy=1
            accuracies+=1
                
    #Check for red accs
    for die in reds:
        if die == 3:
            accuracy=1
            accuracies+=1
                
    ###THE REST OF CF###
    if (len(reds) > 0 ) and trc_available and crit and cf and not cf_spent:
        reds.append(2)
        damage += 2
        cf_spent = 1
        trc_availabe = 0
        
    elif cf and not cf_spent:
        if len(blacks) >= 1:
            cf_black = ceil(random()*8)
            #if cf_black < 3:               #Audit: Not sure why I gave the black
            #   cf_black = ceil(random()*8) #CF a free reroll here...

            if cf_black > 6:
                crit = 1
                damage += 2
            elif cf_black > 2:
                damage += 1
            blacks.append(cf_black)
        elif len(blues) >= 1:
            cf_blue = ceil(random()*8)
            
            if cf_blue < 3:
                accuracies += 1
                accuracy = 1
            else:
                damage += 1
            blues.append(cf_blue)
        elif len(reds) >= 1:
            cf_red = ceil(random()*8)
            
            if cf_red == 8:
                damage += 2
            elif cf_red == 6-7:
                damage += 1
                crit = 1
            elif cf_red == 4-5:
                damage += 1
            elif cf_red == 3:
                accuracies += 1
                accuracy == 1
            reds.append(cf_red)


    #SENSOR TEAMS
    #Doesn't compare outcomes, strictly checks for accs vs target_accs, so you
    #can end up spending a black h/c to flip a red dbl for less overall dmg
    
    if sensor and (accuracies < acc_target):
    
        #look for a die to spend
        fodder = ""
        for black in enumerate(blacks): #look for a blank black to burn first
            if black[1] < 3:
                fodder = ["black",black[0]]
        for red in enumerate(reds):     #look for a blank red to burn
            if red[1] < 3:
                if not fodder:
                    fodder = ["red",red[0]]
        for blue in enumerate(blues):   #look for a blue to burn
            if blue[1] > 2:
                if not fodder:
                    fodder = ["blue",blue[0]]
        for black in enumerate(blacks): #look for a black hit to burn
            if black[1] < 7:
                if not fodder:
                    fodder = ["black",black[0]]
        for red in enumerate(reds):     #look for a red hit to burn
            if red[1] < 8:
                if not fodder:
                    fodder = ["red",red[0]]
        for red in enumerate(reds):     #look for a red double to burn
            if not fodder:
                fodder = ["red",red[0]]
        for black in enumerate(blacks): #look for a black h/c to burn
            if not fodder:
                fodder = ["black",black[0]]
                
        #look for a candidate to flip to acc
        flipper = ""
        if fodder and ((len(blues) > 0) or (len(reds) > 0)):
            flipper = ""
            for red in enumerate(reds):     #look for a blank red to burn
                if red[1] < 3:
                    flipper = ["red",red[0]]
                    if flipper == fodder: flipper = ""
            for blue in enumerate(blues):   #look for a blue to burn
                if blue[1] > 2:
                    if not flipper:
                        flipper = ["blue",blue[0]]
                        if flipper == fodder: flipper = ""
            for red in enumerate(reds):     #look for a red hit to burn
                if red[1] < 8:
                    if not flipper:
                        flipper = ["red",red[0]]
                        if flipper == fodder: flipper = ""
            for red in enumerate(reds):     #look for a red double to burn
                if not flipper:
                    flipper = ["red",red[0]]
                    if flipper == fodder: flipper = ""

        if flipper:
            blacklist, bluelist, redlist = list(blacks), list(blues), list(reds)
            if flipper[0] == "red":
                redlist[flipper[1]] = 3
                accuracies += 1
                accuracy = 1
            else: 
                bluelist[flipper[1]] = 1
                accuracies += 1
                accuracy = 1
            if fodder[0] == "black":
                del blacklist[fodder[1]]
            elif fodder[0] == "red":
                del redlist[fodder[1]]
            elif fodder[0] == "blue":
                del bluelist[fodder[1]]
            
            blacks, blues, reds = tuple(blacklist), tuple(bluelist), tuple(redlist)
            
    #H9
    #Doesn't check outcomes, just flips the lowest-damage red or blue if we're
    #short of the target number of accs (1 by default)
    
    if h9 and (accuracies < acc_target):

        #look for a candidate to flip to acc
        flipper = ""
        if (len(blues) > 0) or (len(reds) > 0):
            flipper = ""
            for red in enumerate(reds):     #look for a blank red to burn
                if red[1] < 3:
                    flipper = ["red",red[0]]
            for blue in enumerate(blues):   #look for a blue to burn
                if blue[1] > 2:
                    if not flipper:
                        flipper = ["blue",blue[0]]
            for red in enumerate(reds):     #look for a red hit to burn
                if red[1] < 8:
                    if not flipper:
                        flipper = ["red",red[0]]
            for red in enumerate(reds):     #look for a red double to burn
                if not flipper:
                    flipper = ["red",red[0]]

        if flipper:
            blacklist, bluelist, redlist = list(blacks), list(blues), list(reds)
            if flipper[0] == "red":
                redlist[flipper[1]] = 3
                accuracies += 1
                accuracy = 1
            else: 
                bluelist[flipper[1]] = 1
                accuracies += 1
                accuracy = 1
            
            blacks, blues, reds = tuple(blacklist), tuple(bluelist), tuple(redlist)
 
    #Black damage total
    for x in blacks:
        if x > 6: crit=1
    
    if not crit:
        fails+=1
        
    for die in blacks:
        if die > 6: damage += 2
        elif die > 2: damage += 1
                
    #Blue damage total   
    for die in blues:
        if die > 2: damage += 1
        else:
            accuracy=1
                
    #Red damage total
    for die in reds:
        if die > 7: damage += 2
        elif (die > 5) and salvation: damage += 2
        elif die > 3: damage += 1
        elif die == 3: 
            accuracy=1
            
    #Brace
    braced_damage = ceil(damage/2)

    ###FINALIZE EACH ITERATION###        
        
    if acm and ((7 in blacks) or (8 in blacks)): damage,braced_damage = [x + 2 for x in [damage,braced_damage]]
    if apt and ((7 in blacks) or (8 in blacks)): damage,braced_damage = [x + 1 for x in [damage,braced_damage]]
    
    if accuracies >= acc_target:
        accuracies_overall+=1
    damage_overall+=damage
    braced_damage_overall+=braced_damage
    fails_overall+=fails
    
    if tries==1:
        print("Blacks:",blacks,"\nBlues:",blues,"\nReds:",reds)
        
    #Did it one-shot a CR90?
    
    if distance == 0:    # close range
        if not accuracy:
            if acm: damage-=1
            if damage >= 8:
                cr90s_killed += 1
        elif accuracy:
            if acm: damage-=2
            if damage >= 6:
                cr90s_killed += 1
                
    #Did it one-shot a Raider?
    
    if distance == 0:    # close range
        if not accuracy:
            if acm: damage-=2
            if apt and (damage >=10):
                raiders_killed += 1
            elif damage >= 11:
                raiders_killed += 1
        elif accuracy:
            if acm: damage-=2
            if damage >= 6:
                raiders_killed += 1
        
if (acm or apt):
    print(str(tries-fails_overall)+" black crits of "+str(tries)+" tries. \n"+
          str((tries-fails_overall)/tries)+" ACM/APT success rate.")
          
print(str(damage_overall/tries)+" average damage.")
if showbrace: print(str(braced_damage_overall/tries)+" average braced damage.")
print(str(round(100*accuracies_overall/tries,2))+"% of rolls hit accuracy target.")
print(str(round(100*cr90s_killed/tries,2))+"% of CR90's one-shotted.")
print(str(round(100*raiders_killed/tries,2))+"% of Raiders one-shotted.")
