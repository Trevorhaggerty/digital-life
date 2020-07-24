
#libraries
import numpy as np
import sys
import random
import datetime

#local import
from printingHandler import *
from inputHandler import *
from eventLog import *
from kmean import *
from nnode import *
from hexTools import *
from terrainGenerator import *


logger = eventLog('Goblin Tentacles Python : cell simulation', '0.1', 5, True)
gameSpace = createTerrain(40, 40,  datetime.datetime.now(), 60, False)
logger.logEvent('terrain generated',5)


def main():
    gameOver = False 
    gameTick = 0
    
    while gameOver == False:
        
        clearScreen()
        logger.logEvent('gameTick:' + str(gameTick) + '--------------------------------------------------------------------------------------',0)
        printGameSpace(gameSpace)

        for i in range(len(gameSpace.entityList)):
            gameSpace.entityList[i].update(gameSpace,gameSpace.entityList)

        gameTick += 1

        if requestContinue() == 'x':
            gameOver = True

        if gameTick > 10000000:
            gameOver = True

   