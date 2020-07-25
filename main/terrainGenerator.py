
import random
from gameSpace import *

from mathTools import *
from hexTools import *
from entities import *


fillerNumberA = -96
fillerNumberB = -69
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
def fillScattered(target,spread, percentChance, gameSpace):
    count = 0
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            if random.randint(0,100) % int(100/percentChance) == 0 and gameSpace.terrainData[x][y] == target:
                gameSpace.terrainData[x][y] = spread
                count += 1
    return count
#------------------------------------------------------------------
def fillSwap(target, spread, gameSpace):
    count = 0
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            if gameSpace.terrainData[x][y] == target:
                gameSpace.terrainData[x][y] = spread
                count += 1
    return count
#-----------------------------------------------------------------------
def fillGaps(target, targetCount, secondTarget, spread, gameSpace): # if a is surrounded by b many c's make a become d
    count = 0
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            holeCheck = sum(checkNeighbor(x, y, secondTarget, gameSpace))
            if holeCheck > targetCount and gameSpace.terrainData[x][y] == target :
                gameSpace.terrainData[x][y] = spread
                count += 1
    return count
#-----------------------------------------------------------------------
def fillEdges(target, secondTarget, spread, gameSpace): # if a is touching any b make a become c
    count = 0
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            edgesDetected = sum(checkNeighbor(x, y, secondTarget, gameSpace))
            if gameSpace.terrainData[x][y] == target and edgesDetected > 0:
                gameSpace.terrainData[x][y] = spread
                count += 1
    return count
#---------------------------------------------------------------------------
def fillBoarder(spread, gameSpace):
    count = 0
    for i in range(gameSpace.xMax):
        gameSpace.terrainData[i][0] = spread
        gameSpace.terrainData[i][gameSpace.yMax - 1] = spread
        count +=2
    for i in range(gameSpace.yMax):
        gameSpace.terrainData[0][i] = spread
        gameSpace.terrainData[gameSpace.xMax - 1][i] = spread
        count +=2
    return count
#----------------------------------------------------------------------------
def fillBCurve(x1 , y1, x2, y2, target, spread, h, gameSpace):
    count = 0
    x3 = random.randint(0, int(gameSpace.xMax / (4 * h)))
    y3 = random.randint(0, int(gameSpace.yMax / (4 * h)))
    h = h * 10
    k = 0
    while k < 1 :
        for y in range(gameSpace.yMax):
            for x in range(gameSpace.xMax):
                if (x >= int(((1 - (k)) * (1 - (k)) * (x1) + h * (1 - (k)) * (k) *	(x3 ) + (k) * (k) * (x2)))
				and y >= int(((1 - (k)) * (1 - (k)) * (y1) + h * (1 - (k)) * (k) *	(y3 ) + (k) * (k) * (y2)))													
				and x <= int(((1 - (k)) * (1 - (k)) * (x1) + h * (1 - (k)) * (k) *	(x3 ) + (k) * (k) * (x2)))
				and y <= int(((1 - (k)) * (1 - (k)) * (y1) + h * (1 - (k)) * (k) *	(y3 ) + (k) * (k) * (y2)))) :
                    if gameSpace.terrainData[x][y] == target:
                        gameSpace.terrainData[x][y] = spread
                        count +=1
        k += 0.005
#---------------------------------------------------------------------------------

def bucketFill(x , y, target, spread, gameSpace):
    gameSpace.terrainData[x][y] = fillerNumberA
    spreading = 1
    while spreading > 0:
        change = fillEdges(target,fillerNumberA,fillerNumberB,gameSpace)
        change += fillEdges(target,fillerNumberB,fillerNumberA,gameSpace)
        spreading = change
    fillSwap(fillerNumberA, fillerNumberB, gameSpace)
    count = fillSwap(fillerNumberB,spread,gameSpace)
    return count

#--------------------------------------------------------------------------------
def countHexType(target, gameSpace):
    count = 0
    for y in range(gameSpace.yMax):
        for x in range(gameSpace.xMax):
            if gameSpace.terrainData[x][y] == target:
                count += 1
    return count
#--------------------------------------------------------------------

def createTerrain(xMax, yMax, seed, spaciousness , water):
    gs = gameSpace(xMax, yMax)
    random.seed(seed)
    fillScattered(0,1, 100 - spaciousness, gs)
    fillGaps(0, 4, 1 , 1, gs)
    fillGaps(1, 3, 0 , 0, gs)
    fillSwap(1, 2, gs)
    fillBoarder(2, gs)
    fillEdges(0, 2 , 1 , gs)
    #gs.entityList.append(cell(random.randint(int(gs.xMax/7), int(gs.xMax*6/7)),random.randint(int(gs.yMax/7), int(gs.yMax*6/7)),[0,0,0,0]))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))    
    gs.entityList.append(food(random.randint(int(gs.xMax/7), int(gs.xMax*6/7)),random.randint(int(gs.yMax/7), int(gs.yMax*6/7)),3,rndID()))
    gs.entityList.append(food(random.randint(int(gs.xMax/7), int(gs.xMax*6/7)),random.randint(int(gs.yMax/7), int(gs.yMax*6/7)),3,rndID()))
    gs.entityList.append(food(random.randint(int(gs.xMax/7), int(gs.xMax*6/7)),random.randint(int(gs.yMax/7), int(gs.yMax*6/7)),3,rndID()))
    

    fillBoarder(1, gs)
    fillEdges(2, 0 , 1 , gs)
    fillSwap(2, 1, gs)
    for i in gs.entityList:
        fillLandingZone(i.x , i.y , 0, gs)
        for j in gs.entityList:
            fillBCurve(i.x, i.y, j.x, j.y,1, 3 , 4, gs)
    
    fillSwap(0, 3, gs)
    bucketFill(gs.entityList[0].x,gs.entityList[0].y, 3, 0, gs)
    fillEdges(1,0,2, gs)
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))
    gs.entityList.append(cell(int(gs.xMax/2),int(gs.yMax/2),[0,0,0,0],rndID()))

    return gs