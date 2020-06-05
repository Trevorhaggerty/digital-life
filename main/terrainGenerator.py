
import random
from gameSpace import *

from hexTools import *
from entities import *
random.seed(420)

#----------------------------------------------------------------------------------------
def fillLandingZone(x, y, spread, gameSpace):
    if x <= 2:
        x += 2
    elif x >= gameSpace.xMax:
        x -= 2

    if y <= 2:
        y += 2
    elif y >= gameSpace.yMax:
        y -= 2
    
    gameSpace.terrainData[x][y] = spread
    if (y % 2 != 0) :
        gameSpace.terrainData[x - 1][y - 1] = spread
        gameSpace.terrainData[x - 0][y - 1] = spread
        gameSpace.terrainData[x - 1][y + 0] = spread
        gameSpace.terrainData[x + 1][y + 0] = spread
        gameSpace.terrainData[x - 1][y + 1] = spread
        gameSpace.terrainData[x + 0][y + 1] = spread

    elif y % 2 == 0:	 		  
        gameSpace.terrainData[x + 0][y - 1] = spread
        gameSpace.terrainData[x + 1][y - 1] = spread
        gameSpace.terrainData[x - 1][y + 0] = spread
        gameSpace.terrainData[x + 1][y + 0] = spread
        gameSpace.terrainData[x + 0][y + 1] = spread
        gameSpace.terrainData[x + 1][y + 1] = spread
    return 0
#----------------------------------------------------------------------
def fillScattered(spread, percentChance, gameSpace):
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            if random.randint(0,100) % int(100/percentChance) == 0:
                gameSpace.terrainData[x][y] = spread
    return 0
#------------------------------------------------------------------
def fillSwap(target, spread, gameSpace):
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            if gameSpace.terrainData[x][y] == target:
                gameSpace.terrainData[x][y] = spread
    return 0
#-----------------------------------------------------------------------
def fillGaps(target, targetCount, secondTarget, spread, gameSpace): # if a is surrounded by b many c's make a become d
    holesFilled = 0
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            holeCheck = sum(checkNeighbor(x, y, secondTarget, gameSpace))
            if holeCheck > targetCount and gameSpace.terrainData[x][y] == target :
                gameSpace.terrainData[x][y] = spread
                holesFilled += 1
    return holesFilled
#-----------------------------------------------------------------------
def fillEdges(target, secondTarget, spread, gameSpace):
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            edgesDetected = sum(checkNeighbor(x, y, secondTarget, gameSpace))
            if gameSpace.terrainData[x][y] == target and edgesDetected > 0:
                gameSpace.terrainData[x][y] = spread
    return 0
#---------------------------------------------------------------------------
def fillBoarder(spread, gameSpace):
    for i in range(gameSpace.xMax):
        gameSpace.terrainData[i][0] = spread
        gameSpace.terrainData[i][gameSpace.yMax - 1] = spread
    for i in range(gameSpace.yMax):
        gameSpace.terrainData[0][i] = spread
        gameSpace.terrainData[gameSpace.xMax - 1][i] = spread
    return 0
#----------------------------------------------------------------------------
def fillBCurve(x1 , y1, x2, y2, spread, hallWidth, gameSpace):
    x3 = random.randint(0, int(gameSpace.xMax / 2))
    y3 = random.randint(0, int(gameSpace.yMax / 2))
    hallWidth = hallWidth * 10
    k = 0
    while k < 1 :
        for y in range(gameSpace.yMax):
            for x in range(gameSpace.xMax):
                if (x >= int(((1 - (k)) * (1 - (k)) * (x1) + hallWidth * (1 - (k)) * (k) *	(x3 ) + (k) * (k) * (x2)))
				and y >= int(((1 - (k)) * (1 - (k)) * (y1) + hallWidth * (1 - (k)) * (k) *	(y3 ) + (k) * (k) * (y2)))													
				and x <= int(((1 - (k)) * (1 - (k)) * (x1) + hallWidth * (1 - (k)) * (k) *	(x3 ) + (k) * (k) * (x2)))
				and y <= int(((1 - (k)) * (1 - (k)) * (y1) + hallWidth * (1 - (k)) * (k) *	(y3 ) + (k) * (k) * (y2)))) :
                    gameSpace.terrainData[x][y] = spread
        k += 0.01

def createTerrain(xMax, yMax, seed, water):
    gs = gameSpace(xMax, yMax)
    random.seed(seed)
    #fillScattered(1,100, gs)
    #fillGaps(0, 4, 1 , 1, gs)
    #fillGaps(1, 3, 0 , 0, gs)
    #fillSwap(1, 2, gs)
    #fillBoarder(2, gs)
    #fillEdges(0, 2 , 1 , gs)
    gs.entityList.append(playerEntity(random.randint(3, xMax - 3), random.randint(3, yMax - 3)))
    gs.entityList.append(monsterEntity(int(xMax/2), int(yMax/2)))

    fillBoarder(1, gs)
    #fillEdges(2, 0 , 1 , gs)
    #fillSwap(2, 1, gs)
    #for i in gs.entityList:
    #    fillLandingZone(i.x , i.y , 0, gs)
    #    for j in gs.entityList:
    #        fillBCurve(i.x, i.y, j.x, j.y, 0, .5, gs)
    
    return gs