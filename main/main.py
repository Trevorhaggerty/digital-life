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
gameRange = [20, 20]
gameSpace = [ ["  " for x in range(gameRange[1]) ] for x in range(gameRange[0]) ]
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

basicDNA = [1, .001 , 200, "㋺", 2, 6]

cell(basicDNA, random.randint(0,gameRange[0]-1), random.randint(0,gameRange[1]-1), len(entityList))

population = 0
desiredPopulation = 5
while population < desiredPopulation :
    entityList.append( cell(basicDNA, random.randint(0,gameRange[0]-1), random.randint(0,gameRange[1]-1), len(entityList)) )
    entityList[-1].mutate()
    population = len(entityList)

gameStartTime = datetime.datetime.now()

entityList.append(foodPellet(int(gameRange[0]/2),int(gameRange[1]/2),5, len(entityList)))


#mainloop----------------------------------------

end = False
lastFrame = datetime.datetime.now()


while end == False and gameTick <= gameTimeLimit:
    sleep(.5)
    clearScreen()

    for i in range(len(entityList)):
        entityList[i].update(gameSpace, entityList)
        #print(entityList[i].info())
    

    printGameSpace(gameSpace, entityList,gameRange[0], gameRange[1])
    gameTick += 1
    gameTimeRunning = (datetime.datetime.now() - gameStartTime).total_seconds()
    refreshElement = (datetime.datetime.now() - lastFrame).total_seconds()
    refreshSum.append(refreshElement)

    #for i in range(len(entityList)):
    #    if entityList[i].entityType == 2 :
    #        print(entityList[i].neuron.info())

    print('average tick time = ' + str(sum(refreshSum,0) / gameTick))
    print('time since game began = ' + str(gameTimeRunning))
    print('game tick = ' + str(gameTick))
    lastFrame = datetime.datetime.now()
    sleep(.5)
    
    #sleep(1)
    #valuedCustomerInput = input("enter to continue. type enter to end\n")
    #valuedCustomerInput = str.casefold(valuedCustomerInput)
    #if valuedCustomerInput == 'enter':
    #    end = True
    