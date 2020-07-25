
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
gs = createTerrain(30, 30,  datetime.datetime.now(), 69, False)
entl = gs.entityList
logger.logEvent('terrain generated',5)


def main():
    gameOver = False 
    gameTick = 0
    
    while gameOver == False:


    
        #clearScreen()
        #logger.logEvent('gameTick:' + str(gameTick) + '--------------------------------------------------------------------------------------',0)
        printGameSpace(gs)

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
        if count == 0:
            gameOver = True

        gameTick += 1

        #if gameTick % 50000 == 0:
        #    if requestContinue() == 'x':
        #        gameOver = True
#       
        if gameTick > 12345:
            gameOver = True

        
    for i in entl:
        i.info()
   