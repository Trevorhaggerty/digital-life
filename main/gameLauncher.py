# a conversion of a very early working prototype of goblinTentacles,
# mainly the functionality of 0.3 and the level generation of 0.5-0.7

#libraries
import datetime
import numpy as np
import sys
import random

#local import
from printingHandler import *
from inputHandler import *
from eventLog import *

from terrainGenerator import *


#global variable declarations



#global class objects

logger = eventLog('Goblin Tentacles Python', '0.1?', 5)
gameSpace = createTerrain(30, 20, 987698, False)
logger.logEvent('terrain generated',5)

def main():
    gameOver = False
    gameTick = 0
    while gameOver == False:
        printGameSpace(gameSpace)

        
        
        for i in range(len(gameSpace.entityList)):
            print(str(gameSpace.entityList[i].ID))
            if gameSpace.entityList[i].ID == str('player'):
                directionRequested = requestMovementInput()
                if directionRequested == -1:
                    gameOver = True
                gameOver = moveEntity(i, directionRequested,gameSpace)
            elif gameSpace.entityList[i].ID == 'monster':
                gameOver = moveEntity(i, random.randint(0,5),gameSpace)

        gameTick += 1
        if gameTick > 100:
            gameOver = True


main()