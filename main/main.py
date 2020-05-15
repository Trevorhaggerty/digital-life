#Digital life
#
#
#
#local imports --------------------------------
from neuron import *
from gameSpace import *
from cell import *

#imports from python libraries-----------------
import datetime

from os import system, name 
from time import *
import random

#global variables------------------------------
gameRange = [40, 40 ]
gameSpace = [["  " for x in range(gameRange[1])] for x in range(gameRange[0]) ]
refreshSum = []
gameTick = 0
entityList = []

#global functions-------------------------------
def clearScreen():
	if name == 'nt': 
		_ = system('cls') 
	else: 
		_ = system('clear') 
#main Pre loop-----------------------------------
userInputForGameTimeLim = input ("Enter how long to run the program in Ticks: ")
gameTimeLimit = int(userInputForGameTimeLim)

basicDNA = [1, .0001 , 200, "㋺", 6, 0]
cell1 = cell(basicDNA, 3, 3, len(entityList))
entityList.append(cell1)
gameStartTime = datetime.datetime.now()

entityList.append(foodPellet(8,9,5, len(entityList)))


#mainloop----------------------------------------

end = False
lastFrame = datetime.datetime.now()


while end == False and gameTick <= gameTimeLimit:

    clearScreen()

    printGameSpace(gameSpace, entityList,gameRange[0], gameRange[1])
    for i in range(len(entityList)):
        entityList[i].update(gameSpace, entityList)
        #print(entityList[i].info())
    

    gameTick += 1
    gameTimeRunning = (datetime.datetime.now() - gameStartTime).total_seconds()
    refreshElement = (datetime.datetime.now() - lastFrame).total_seconds()
    refreshSum.append(refreshElement)
    print('average tick time = ' + str(sum(refreshSum,0) / gameTick))
    print('time since game began = ' + str(gameTimeRunning))
    print('game tick = ' + str(gameTick))
    lastFrame = datetime.datetime.now()
    sleep(.05)
    
    #sleep(1)
    #valuedCustomerInput = input("enter to continue. type enter to end\n")
    #valuedCustomerInput = str.casefold(valuedCustomerInput)
    #if valuedCustomerInput == 'enter':
    #    end = True
    