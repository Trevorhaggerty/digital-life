#testing git hub
#s
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

gameRange = [15,15]
gameSpace = [["  " for x in range(gameRange[1])] for x in range(gameRange[0])]
refreshSum = []
gameTick = 0
entityList = []

#global functions-------------------------------
def clearScreen():
	if name == 'nt': 
		_ = system('cls') 
	else: 
		_ = system('clear') 
#same ^^^^^^^^^^^^^^^^^^^^^^^^^^
###functiion i found on the internet > def loading(count):
###functiion i found on the internet >     all_progress = [0] * count
###functiion i found on the internet >     sys.stdout.write("\n" * count) # Make sure we have space to draw the bars
###functiion i found on the internet >     while any(x < 100 for x in all_progress):
###functiion i found on the internet >         time.sleep(0.01)
###functiion i found on the internet >         # Randomly increment one of our progress values
###functiion i found on the internet >         unfinished = [(i, v) for (i, v) in enumerate(all_progress) if v < 100]
###functiion i found on the internet >         index, _ = random.choice(unfinished)
###functiion i found on the internet >         all_progress[index] += 1
###functiion i found on the internet >         
###functiion i found on the internet >         # Draw the progress bars
###functiion i found on the internet >         sys.stdout.write(u"\u001b[1000D") # Move left
###functiion i found on the internet >         sys.stdout.write(u"\u001b[" + str(count) + "A") # Move up
###functiion i found on the internet >         for progress in all_progress: 
###functiion i found on the internet >             width = progress / 4
###functiion i found on the internet >             print "[" + "#" * width + " " * (25 - width) + "]"
###functiion i found on the internet >         


#main Pre loop-----------------------------------
userInputForGameTimeLim = input ("Enter how long to run the program in Minutes: ")
gameTimeLimitMin = int(userInputForGameTimeLim)
gameTimeLimitSec = gameTimeLimitMin * 60

basicDNA = [1, .005 , 120, "㋺"]
cell1 = cell(basicDNA, 3, 3, len(entityList))
entityList.append(cell1)
gameStartTime = datetime.datetime.now()

entityList.append(foodPellet(8,9,5, len(entityList)))


#mainloop----------------------------------------

#testing dendrites, feeding data direct rather than through the synapse

end = False
lastFrame = datetime.datetime.now()
while end == False and (datetime.datetime.now() - gameStartTime).total_seconds() <= gameTimeLimitSec:


    ##for testing --------------------------------------------------------------------------------------
     #
    #for i in range(len(entityList)):
    #
    #    if sum(entityList[i].axon.telodendrites) != 0 and entityList[i].axon.feedingForward == True:
    #        j = 0
    #        while j < len(entityList[i].axon.telodendrites):
    #            entityList[i].axon.telodendrites[j] = 0
    #            j += 1
    #    if sum(entityList[i].dendrite.dendriticTree) != 0 and entityList[i].dendrite.backFlowing == True:
    #        j = 0
    #        while j < len(entityList[i].dendrite.dendriticTree):
    #            entityList[i].dendrite.dendriticTree[j] = 0
    #            j += 1
#
    ##
    #for i in range(len(entityList)) :
    #    if gameTick % 5 == 0 :
    #        entityList[i].dendrite.dendriticTree[0] = 0
    #        entityList[i].dendrite.dendriticTree[1] = 1
    #    if gameTick % 5 == 3 :
    #        entityList[i].axon.telodendrites[0] = 1
#
    #-------------------------------------------------------------------------------------------------------
    
    clearScreen()

    printGameSpace(gameSpace, entityList,gameRange[0], gameRange[1])
    for i in range(len(entityList)):
        #print(entityList[i].info())
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
    