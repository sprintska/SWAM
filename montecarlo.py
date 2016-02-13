#!/usr/bin/python3.4
#!python

'''To run this script, make sure you have Python 3 installed, then type
py path/to/script/montecarlo.py on the command line.  It was written and
tested for Python 3.4.  If you have Python 2, go get 3 and stop being a
weiner.  If you have a newer version, hello from the distant past!

This is a Monte Carlo simulation script built to model expected damage 
profiles in Star Wars Armada.  It's pretty rudimentary.  If you don't 
know Python, you should only change the variables under OPTIONS.  To add
the effect of an upgrade, set the variable equal to 1; to remove it, set
it to 0. The color_base variables set the number of dice in the pool.'''

from random import *
from math import *

#####OPTIONS (Set to 1 for yes, 0 for no)#####

tries=1					# how many iterations to try
cf=0					# concentrate fire available?
trc=0					# TRC available?
black_base=0			# number of black dice (base)
blue_base=4				# number of blue dice (base)
red_base=4				# number of red dice (base)
acm=0					# ACM available?
apt=0					# APT available?
ackbar=0				# Ackbar available?
oe=0					# OE available?
vader=0					# Vader available?
leading_shots=0			# LS available?
distance=0				# Range: 0 for close, 1 for medium, 2 for long
dist_override_black=0 	# Distance override for blacks (e.g., Defiant)
dist_override_blue=0  	# Distance override for blues (e.g., Defiant)

##############################################

# Initialize some variables
damage_overall=0		# Total damage
accuracies_overall=0	# How many times we got at least 1 acc
fails_overall=0					# How many times we failed to get a black crit

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
	if ackbar and red_base: red_base += 2
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
	if not leading_shots:
		for red in enumerate(reds):
			if red[1] <= 2: 
				reds[red[0]]=ceil(random()*8)
			elif (red[1] == 3) and not accuracy:
				accuracy = 1
			elif (red[1] == 3) and accuracy:
				reds[red[0]]=ceil(random()*8)				
	#If we have LS, fish for doubles
	elif leading_shots and blues:
		for red in enumerate(reds):
			if (red[1] != 3) and (red[1] != 8): 
				reds[red[0]]=ceil(random()*8)
			elif (red[1] == 3) and not accuracy:
				accuracy = 1
			elif (red[1] == 3) and accuracy:
				reds[red[0]]=ceil(random()*8)
	
	
	#Count damage
	for die in reds:
		if die > 7: damage += 2
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
