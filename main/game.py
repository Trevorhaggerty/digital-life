
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


def main():
    gs = createTerrain(30, 30, 420, 69, False)#datetime.datetime.now(), 69, False)
    entl = gs.entityList
    logger.logEvent('terrain generated',5)
    startTime = time.time()
    currentTime = (time.time() - startTime)
    while currentTime < 5000:
        currentTime = (time.time() - startTime)
        
        gameOver = False 
        gameTick = 0
        gs = createTerrain(30, 30, datetime.datetime.now(), 69, False)
        entl = gs.entityList

        while gameOver == False:
        
            #clearScreen()
            #logger.logEvent('gameTick:' + str(gameTick) + '--------------------------------------------------------------------------------------',0)
            printGameSpace(gs)
            currentTime = (time.time() - startTime)
            
            print(str(currentTime))

            count = 0
            j = -2
            for i in range(len(entl)):
                entl[i].update(gs,entl)
                if entl[i].HP <= 0:  
                    j = i
                if entl[i].type == 'monster':
                    count +=1
            if j >= 0:
                del entl[j]
            if count <= 2:
                for ent in entl:
                    ent.info()
                    printGameSpace(gs)
                gameOver = True

            logger.logEvent('gameTicks : ' + str(gameTick),5)
            gameTick += 1
            #if gameTick % 50000 == 0:
            #    if requestContinue() == 'x':
            #        gameOver = True
#           
            if gameTick > 10000:
                for ent in entl:
                    ent.info()
                    printGameSpace(gs)
                gameOver = True
        
        
   