from gameSpace import *
from cell import *
import datetime
from os import system, name 
from time import sleep 
import random


gameStartTime = datetime.datetime.now()
gameRange = [20,10]
gameSpace = [["  " for x in range(gameRange[1])] for x in range(gameRange[0])]
entitylist = []




def printInfo(gameSpace, entitylist) :
    print("There are "+ str(len(entitylist)) +" entities present on the gameSpace")
    for x in entitylist :
        print(x.info())

def clearScreen(): #not my function
	if name == 'nt': 
		_ = system('cls') 
	else: 
		_ = system('clear') 



#DNA = [randomSeed, healingFactor, maturityAge, appearanceString]
basicDNA = [2, .1 , 10, "毜"]
basicDNA2 = [8, .01 , 20, "㋺"]

entitylist.append(cell(basicDNA, 5, 6, len(entitylist)))
entitylist.append(cell(basicDNA2, 10, 5, len(entitylist)))

entitylist.append(foodPellet(3,3,5, len(entitylist)))

#mainloop
end = False
while end == False:
    clearScreen()
    updateGameSpace(gameSpace, entitylist, gameRange[0], gameRange[1])
    printGameSpace(gameSpace, entitylist, gameRange[0], gameRange[1])
    printInfo(gameSpace, entitylist)
    #print("There are "+ str(len(entitylist)) +" entities present on the gameSpace")
    sleep(.01) 

    
    if (datetime.datetime.now() - gameStartTime).total_seconds() >= 200 :
        end = True
