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
from hexTools import *
from terrainGenerator import *



#global stuff
def clearScreen():
    if name == 'nt': 
	    _ = system('cls')
    else: 
	    _ = system('clear') 

logger = eventLog('Goblin Tentacles Python', '0.1', 5, True)
gameSpace = createTerrain(20, 20, 2, False)
logger.logEvent('terrain generated',5)




def main():
    gameOver = False
    gameTick = 0
    while gameOver == False:
        clearScreen()
        logger.logEvent('gameTick:' + str(gameTick) + '--------------------------------------------------------------------------------------',0)
        printGameSpace(gameSpace)

        
        #_------------------------this will likely end up being a seperate file soon
#--------------------------------------------------------------------------------------------------------------------------------------------
        for i in range(len(gameSpace.entityList)):
#--------------------------------------------------------------------------------------------------------------------------------------------
            if gameSpace.entityList[i].ID == str('player'):
                #gameSpace.entityList[i].x = np.random.randint(1,gameSpace.xMax - 1)
                #gameSpace.entityList[i].y = np.random.randint(1,gameSpace.yMax - 1)
                #continue
                directionRequested = requestMovementInput()
                if directionRequested == -1:
                    gameOver = True
                moveEntity(i, directionRequested,gameSpace)
#--------------------------------------------------------------------------------------------------------------------------------------------
            elif gameSpace.entityList[i].ID == 'monster':
                #print(distance(gameSpace.entityList[i].x, gameSpace.entityList[i].y, gameSpace.entityList[0].x, gameSpace.entityList[0].y))
                monsterSenses = []
                if gameSpace.entityList[i].x > gameSpace.entityList[0].x:
                    #monsterSenses.append(2 * (sigmoid(distance(gameSpace.entityList[i].x, 0, gameSpace.entityList[0].x, 0)) - 0.5))
                    monsterSenses.append(1)
                    monsterSenses.append(0)
                    
                else:
                    monsterSenses.append(0)
                    monsterSenses.append(1)
                    #monsterSenses.append(2 * (sigmoid(distance(gameSpace.entityList[i].x, 0, gameSpace.entityList[0].x, 0)) - 0.5))

                if gameSpace.entityList[i].y > gameSpace.entityList[0].y:
                    #monsterSenses.append(2 * (sigmoid(distance( 0, gameSpace.entityList[i].y, 0, gameSpace.entityList[0].y)) - 0.5))
                    monsterSenses.append(1)
                    monsterSenses.append(0)
                else:
                    monsterSenses.append(0)
                    monsterSenses.append(1)
                    #monsterSenses.append(2 * (sigmoid(distance( 0, gameSpace.entityList[i].y, 0,  gameSpace.entityList[0].y)) - 0.5))
                #-----------------------------------------------------------------------------------------------
                #monsterSensesBuffer = checkNeighbor(gameSpace.entityList[i].x, gameSpace.entityList[i].y, 1, gameSpace)
                #for j in range(len(monsterSensesBuffer)):
                #    monsterSenses.append(monsterSensesBuffer.pop())                 
                #
                #logger.logEvent(str(monsterSenses),0)

#--------------------------------------------------------------------------------------------------------------------------------------------
                gameSpace.entityList[i].monsterAI.feedForward(np.array(monsterSenses))
                distanceBeforeMovement = distance(gameSpace.entityList[i].x, gameSpace.entityList[i].y, gameSpace.entityList[0].x, gameSpace.entityList[0].y)
                logger.logEvent("monsterAI output:" + str(gameSpace.entityList[i].monsterAI.outputSignals),0)
#--------------------------------------------------------------------------------------------------------------------------------------------
                if int(gameSpace.entityList[i].monsterAI.outputSignals[0] * 10) > 8:
                    moveEntity(i,0,gameSpace)
                elif int(gameSpace.entityList[i].monsterAI.outputSignals[1] * 10) > 8:
                    moveEntity(i,1,gameSpace)
                elif int(gameSpace.entityList[i].monsterAI.outputSignals[2] * 10) > 8:
                    moveEntity(i,2,gameSpace)
                elif int(gameSpace.entityList[i].monsterAI.outputSignals[3] * 10) > 8:
                    moveEntity(i,3,gameSpace)
                elif int(gameSpace.entityList[i].monsterAI.outputSignals[4] * 10) > 8:
                    moveEntity(i,4,gameSpace)
                elif int(gameSpace.entityList[i].monsterAI.outputSignals[5] * 10) > 8:
                    moveEntity(i,5,gameSpace)
                
                                                        #"0               1")
                                                        #"     ↖ /  \ ↗   ")
                                                        #"5  ⬅ |     |➡  2")
                                                        #"     ↙ \  / ↘    ")
                                                        #"4               3")
#--------------------------------------------------------------------------------------------------------------------------------------------
                distanceAfterMovement = distance(gameSpace.entityList[i].x, gameSpace.entityList[i].y, gameSpace.entityList[0].x, gameSpace.entityList[0].y)

                if (monsterSenses[0] + monsterSenses[1]) > (monsterSenses[2] + monsterSenses[3]):
                    if monsterSenses[0] > monsterSenses[1]:
                        gameSpace.entityList[i].monsterAI.backPropagation([0,0,0,0,0,1])
                        logger.logEvent('[0,0,0,0,0,1] is answer fed',0)
                    else:
                        gameSpace.entityList[i].monsterAI.backPropagation([0,0,1,0,0,0])
                        logger.logEvent('[0,0,1,0,0,0] is answer fed',0)
                else:
                    if monsterSenses[2] > 0:
                        if monsterSenses[0] > monsterSenses[1]:
                            gameSpace.entityList[i].monsterAI.backPropagation([1,0,0,0,0,0])
                            logger.logEvent('[1,0,0,0,0,0] is answer fed',0)
                        else:
                            gameSpace.entityList[i].monsterAI.backPropagation([0,1,0,0,0,0])
                            logger.logEvent('[0,1,0,0,0,0] is answer fed',0)
                    else:
                        if monsterSenses[0] > monsterSenses[1]:
                            gameSpace.entityList[i].monsterAI.backPropagation([0,0,0,0,1,0])
                            logger.logEvent('[0,0,0,0,1,0] is answer fed',0)
                        else:
                            gameSpace.entityList[i].monsterAI.backPropagation([0,0,0,1,0,0])
                            logger.logEvent('[0,0,0,1,0,0] is answer fed',0)
#--------------------------------------------------------------------------------------------------------------------------------------------
                






        gameTick += 1
        if gameTick > 1000:
            gameOver = True

    logger.logEvent('monsters weights per layer per node',0)
    logger.logEvent('inputlayer:',0)
    for i in range(len(gameSpace.entityList[1].monsterAI.inputLayer)):
        logger.logEvent(str(gameSpace.entityList[1].monsterAI.inputLayer[i].weights),0)
    logger.logEvent('hiddenlayer:',0)
    for i in range(len(gameSpace.entityList[1].monsterAI.hiddenLayer)):
        logger.logEvent(str(gameSpace.entityList[1].monsterAI.hiddenLayer[i].weights),0)
    logger.logEvent('outputlayer:',0)
    for i in range(len(gameSpace.entityList[1].monsterAI.outputLayer)):
        logger.logEvent(str(gameSpace.entityList[1].monsterAI.outputLayer[i].weights),0)

main()