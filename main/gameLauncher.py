# a conversion of a very early working prototype of goblinTentacles,
# mainly the functionality of 0.3 and the level generation of 0.5-0.7

#libraries
import datetime
import numpy as np
import sys
from os import system, name 
import random

#local import
from printingHandler import *
from inputHandler import *
from eventLog import *
from nnode import *
from terrainGenerator import *



#global stuff
def clearScreen():
    if name == 'nt': 
	    _ = system('cls')
    else: 
	    _ = system('clear') 

logger = eventLog('Goblin Tentacles Python', '0.1', 5)
gameSpace = createTerrain(40, 40, 1, False)
logger.logEvent('terrain generated',5)
monsterAi = nnode(0, 1, 2)
monsterAi.weights = np.array([-3,2.5])


def main():
    gameOver = False
    gameTick = 0
    while gameOver == False:
        clearScreen()
        logger.logEvent('gameTick:' + str(gameTick),0)
        printGameSpace(gameSpace)

        
        #_------------------------this will likely end up being a seperate file soon
        for i in range(len(gameSpace.entityList)):
            if gameSpace.entityList[i].ID == str('player'):
                
                directionRequested = requestMovementInput()
                if directionRequested == -1:
                    gameOver = True
                gameOver = moveEntity(i, directionRequested,gameSpace)
            elif gameSpace.entityList[i].ID == 'monster':
                #print(distance(gameSpace.entityList[i].x, gameSpace.entityList[i].y, gameSpace.entityList[0].x, gameSpace.entityList[0].y))
                monsterSight = []
                if gameSpace.entityList[i].x > gameSpace.entityList[0].x:
                    monsterSight.append(-distance(gameSpace.entityList[i].x, 0, gameSpace.entityList[0].x, 0))
                else:
                    monsterSight.append(distance(gameSpace.entityList[i].x, 0, gameSpace.entityList[0].x, 0))

                if gameSpace.entityList[i].y > gameSpace.entityList[0].y:
                    monsterSight.append(-distance( 0, gameSpace.entityList[i].y, 0, gameSpace.entityList[0].y))
                else:
                    monsterSight.append(distance( 0, gameSpace.entityList[i].y, 0,  gameSpace.entityList[0].y))
                logger.logEvent(str(monsterSight),0)
                
                monsterAi.inputArray = np.array(monsterSight)
                monsterAi.feedForward()
                
                distanceBeforeMovement = distance(gameSpace.entityList[i].x, gameSpace.entityList[i].y, gameSpace.entityList[0].x, gameSpace.entityList[0].y)
                
                gameOver = moveEntity(i, int(((monsterAi.outputSignal) * 10)/10 * 6),gameSpace)

                distanceAfterMovement = distance(gameSpace.entityList[i].x, gameSpace.entityList[i].y, gameSpace.entityList[0].x, gameSpace.entityList[0].y)

                if abs(monsterSight[0]) > abs(monsterSight[1]):
                    if monsterSight[0] < 0:
                        monsterAi.backPropagationSignal = 1
                    else:
                        monsterAi.backPropagationSignal = 1/2
                else:
                    if monsterSight[1] < 0:
                        if monsterSight[0] < 0:
                            monsterAi.backPropagationSignal = 1/6
                        else:
                            monsterAi.backPropagationSignal = 1/3
                    else:
                        if monsterSight[0] < 0:
                            monsterAi.backPropagationSignal = 5/6
                        else:
                            monsterAi.backPropagationSignal = 2/3

                logger.logEvent('outputsignal' + str(monsterAi.outputSignal), 0)
                logger.logEvent('backpropsignal' + str(monsterAi.backPropagationSignal), 0)
                monsterAi.backPropagation()
                logger.logEvent('weights:' + str(monsterAi.weights), 0)
                






        gameTick += 1
        if gameTick > 10000:
            gameOver = True


main()