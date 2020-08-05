# libraries
import random
from gameSpace import *
# local imports
from mathTools import *
from hexTools import *
from entities import *
from pathfinders import *

# global vars for place holding (also an oppritunity for a childish joke)
fillerNumberA = -916
fillerNumberC = -420
fillerNumberB = -69

# ----------------------------------------------------------------------------------------
#fillswap replaces all tiles of target tiles with a spread tile.
#   if a become b
#   it takes in:
#       - the target tile
#       - the spread tile
#       - the terrainData to effect
#   and it returns:
#       -the number of tiles modified
def fillSwap(target, spread, terrainData):
    #create var for itteration
    count = 0
    #itterate y with a range of 0 to the y axis' max index
    for y in range(len(terrainData[0])):
        #itterate x with a range of 0 to the x axis' max index
        for x in range(len(terrainData)):
            # if the current tile is holds the target tile
            if terrainData[x][y] == target:
                #set the tile to the spread tile
                terrainData[x][y] = spread
                #itterate the counter
                count += 1

    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# scatteredFill
#   replaces hexagons with a target tile with a spread tile. This occurs 
#   based on a percent chance that a tile will be evaluated;
#   if a become b at % chance
#   it takes in:
#       - the target tile
#       - the spread (specified tile to be spread)
#       - the the percent chance of tile evaluation effect
#       - the terrainData to effect
#   and it returns:
#       -the number of tiles modified
def scatteredFill(target, spread, percentChance, terrainData):
    #create var for itteration
    count = 0
    #itterate y with a range of 0 to the y axis' max index
    for y in range(len(terrainData[0])):
        #itterate x with a range of 0 to the x axis' max index
        for x in range(len(terrainData)):
            #choose a random number between 0-99 and evaluate if it is applicable
                # then only if the tile aslo is of the target tile
            if random.randint(0, 100) % int(100/percentChance) == 0 and terrainData[x][y] == target:
                # replace the evaluated tile with the spread tile
                terrainData[x][y] = spread
                #itterate the count
                count += 1
    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# filllandingZone 
#   replaces all the hexagons in a given spot
#   and all its immediate neighbors with a specified tile.;
#   make xy & neighbors become a
#   it takes in:
#       - the x and y locations of the target
#       - the spread (specified tile to be spread)
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def fillLandingZone(x, y, spread, terrainData):
    # adjust the x and y tiles to be within the gamespace
    if x <= 2:
        x += 2
    elif x >= len(terrainData):
        x -= 2

    if y <= 2:
        y += 2
    elif y >= len(terrainData[0]):
        y -= 2
    # make the target location the specified tile
    terrainData[x][y] = spread
    # if even use EvenR even row logic
    if (y % 2 != 0):
        # each tile at the targets neighboring location
        # is set to the specified tile
        terrainData[x - 1][y - 1] = spread
        terrainData[x - 0][y - 1] = spread
        terrainData[x - 1][y + 0] = spread
        terrainData[x + 1][y + 0] = spread
        terrainData[x - 1][y + 1] = spread
        terrainData[x + 0][y + 1] = spread
    # if odd use the EvenR odd row logic
    elif y % 2 == 0:
        # each tile at the targets neighboring location
        # is set to the specified tile
        terrainData[x + 0][y - 1] = spread
        terrainData[x + 1][y - 1] = spread
        terrainData[x - 1][y + 0] = spread
        terrainData[x + 1][y + 0] = spread
        terrainData[x + 0][y + 1] = spread
        terrainData[x + 1][y + 1] = spread
    # if the function is completed successfully return 7 (assumed tiles modified)
    return 7
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#greaterThanFill
#   if a tile with a target tile is surrounded by more than 
#   a specified number of a second target tile modify that tile to a spread tile; 
#   if a is surrounded by b many c's make a become d
#   it takes in:
#       - the target tile
#       - the threshold of 2ndtarget neighbors
#       - the spread tile
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def greaterThanFill(target, targetCount, secondTarget, spread, terrainData):
    #create var for itteration
    count = 0
    #itterate y with a range of 0 to the y axis' max index
    for y in range(len(terrainData[0])):
        #itterate x with a range of 0 to the x axis' max index
        for x in range(len(terrainData)):
            #use the binary check neighbor function and store the sum of the
                #resulting vector to determine how many neighbors are of target tile
            holeCheck = sum(binNeighbor(x, y, secondTarget, terrainData))
            #if the tile has more than the target number of neighbor tiles
                #and the tile is the target tile
            if holeCheck > targetCount and terrainData[x][y] == target:
                # replace the evaluated tile with the spread tile
                terrainData[x][y] = spread
                #itterate the count
                count += 1
    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#lessThanFill
#   modified input to greaterThanFill
#   if a tile with a target tile is surrounded by less than 
#   a specified number of a second target tile modify that tile to a spread tile; 
#   if a is surrounded by less b many c's make a become d
#       - the target tile
#       - the threshold of 2ndtarget neighbors
#       - the spread tile
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def lessThanFill(target, targetCount, secondTarget, spread, terrainData):
    return greaterThanFill(secondTarget, targetCount, target, spread, terrainData)
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#filledges
#   modified input to greaterThanFill
#   if a target tile is in contact with any second target tile become the spread tile   
#   if a is touching any b make a become c
#       - the target tile
#       - the spread tile
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def fillEdges(target, secondTarget, spread, terrainData):
    return greaterThanFill(target, 0, secondTarget, spread, terrainData)
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#fillboarder
#   replaces all tiles at the edges of the terrain with the spread tile
#   if a tile is at the boarder become a
#       - the spread tile
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def fillBoarder(spread, terrainData):
    #create var for itteration
    count = 0
    #itterate through the x locations
    for i in range(len(terrainData)):
        #make all tiles at the top and bottom the spread tile
        terrainData[i][0] = spread
        terrainData[i][len(terrainData[0]) - 1] = spread
        #itterate the count by 2 (each tile modified per step)
        count += 2
    #itterate through the y locations
    for i in range(len(terrainData[0])):
        #make all tiles at the ;eft and right side the spread tile
        terrainData[0][i] = spread
        terrainData[len(terrainData) - 1][i] = spread
        #itterate the count by 2 (each tile modified per step)
        count += 2

    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
#fillbcurve
#   replaces all target tiles with the spread tile that fall on a bcurve determined by
#   two sets of x and y coordinates, the h value 
#   if a is on bcurve become b
#   it takes in:
#       - 2 sets of coordinates
#       - the target tile
#       - the spread tile
#       - the h value
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def fillBCurve(x1, y1, x2, y2, target, spread, h, terrainData):
    #create var for itteration
    count = 0
    #create a random point to use for curvature
    x3 = ((x1 + x2) / 2) + np.random.randint(-3,3)
    y3 = ((y1 + y2) / 2) + np.random.randint(-3,3)
    #set the b curve lerping value to zero
    k = 0
    #begin lerping from point a to point b along the bcurve
    while k < 1:
        #itterate y with a range of 0 to the y axis' max index
        for y in range(len(terrainData[0])):
            #itterate x with a range of 0 to the x axis' max index
            for x in range(len(terrainData)):
                #avoid lerp checks if the tile is not the target type
                if terrainData[x][y] == target:
                    # if the tiles x and y fall on the bcurve
                    if (x >= int(((1 - (k)) * (1 - (k)) * (x1) + h * (1 - (k)) * (k) * (x3) + (k) * (k) * (x2)))
                        and y >= int(((1 - (k)) * (1 - (k)) * (y1) + h * (1 - (k)) * (k) * (y3) + (k) * (k) * (y2)))
                        and x <= int(((1 - (k)) * (1 - (k)) * (x1) + h * (1 - (k)) * (k) * (x3) + (k) * (k) * (x2)))
                        and y <= int(((1 - (k)) * (1 - (k)) * (y1) + h * (1 - (k)) * (k) * (y3) + (k) * (k) * (y2)))):
                        # turn the tile into a spread tile
                        terrainData[x][y] = spread
                        # itterate the count
                        count += 1
        #itterate the lerping value
        k += 0.005
    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------
#bucketFill
#   fills 'regions' of target tile with a spread tile starting at x y coordinates
#   if a is touching a identify as 'region', if 'region' contains x y become b 
#   it takes in:
#       - a set of coordinates
#       - the target tile
#       - the spread tile
#       - the terrain data to effect
#   and it returns:
#       - the number of tiles modified
def bucketFill(x, y, target, spread, terrainData):
    #create var for itteration
    count = 0
    #make the x y tile fillerNumberA
    terrainData[x][y] = fillerNumberA
    #set a value to a positive non 0 number
    delta = 1
    #while tiles are still being replaced (delta > 0)
    while delta > 0:
        #if the target is touching filler A become filler B and record tile count modified
        change = fillEdges(target, fillerNumberA, fillerNumberB, terrainData)
        #if the target is touching filler B become filler A and record tile count modified
        change += fillEdges(target, fillerNumberB, fillerNumberA, terrainData)
        #report to the while loop wether a tile was modified or not
        delta = change
    #make all filler A now filler B
    fillSwap(fillerNumberA, fillerNumberB, terrainData)
    #make all filler B now spread save how many were modified
    count = fillSwap(fillerNumberB, spread, terrainData)

    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#countHexType counts how many of a target tile are on the board
#   if a count +1
#   takes in :
#       - the target tile
#       - the terrain data to analyze
#   returns:
#       - how many target tiles present on board
def countHexType(target, terrainData):
    #create var for itteration
    count = 0
    #itterate y with a range of 0 to the y axis' max index
    for y in range(len(terrainData[0])):
        #itterate x with a range of 0 to the x axis' max index
        for x in range(len(terrainData)):
            # if the tile is the target
            if terrainData[x][y] == target:
                #itterate the count
                count += 1
    #if the function is completed successfully return the number of tiles modified
    return count
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
#createTerrain
#   creates and modifies a gameSpace object, mainly the focus on terrain generation
#   takes in:
#       - the x dimension of the board
#       - the y dimension of the board
#       - seed number
#       - a spaciousness value (0-100)
#       - a bool to see if water is present
#   returns:
#       - populated and modifiied gameSpace object
def createTerrain(xMax, yMax, seed, spaciousness, water):
    #create the gameSpace object
    gs = gameSpace(xMax, yMax)
    #create var to hold terraindata for ease of working
    td = gs.terrainData
    #set the seed to the one given
    random.seed(seed)
    #randomly fill the map with ones and zeros
    scatteredFill(0, 1, 100 - spaciousness, td)
 
    #replace all 0 tiles that have more than 4 1 neighbors into 1 
    greaterThanFill(0, 4, 1, 1, td)
    #replace all 1 tiles that have more than 3 0 neighbors into 0
    greaterThanFill(1, 3, 0, 0, td)
    #replace every 1 tile with a 2 tile
    fillSwap(1, 2, td)
    #make the border tiles 2
    fillBoarder(2, td)
    #replace all 0 tiles touchning a 2 tile with a 1 tile
    fillEdges(0, 2, 1, td)

    #monster creation loop; itterates per range
    for i in range(3):
        #create the monster entity with random locations and 'DNA'
        gs.entityList.append(monster(random.randint(int(gs.xMax/7), int(gs.xMax*6/7)), random.randint(int(gs.yMax/7), int(gs.yMax*6/7)), [10199, np.random.randint(0, 9), 63, 24, np.random.random()], rndID()))

    #food creation loop; itterates per range
    for i in range(3):
        #create three food pellets at random locations throughout the map
        gs.entityList.append(food(random.randint(int(gs.xMax/7), int(gs.xMax*6/7)),
                                random.randint(int(gs.yMax/7), int(gs.yMax*6/7)), 3, rndID()))

    #replace any 2 tile touching a 0 tile to a 1 tile
    fillEdges(2, 0, 1, td)
    #replace all 2 tiles with 1 tiles
    fillSwap(2, 1, td)

    #prepare the terrain for entities
    #itterate throught the enitity list
    for i in gs.entityList:
        #for each entity clear space to spawn
        fillLandingZone(i.x, i.y, 0, td)
        #make a second itteration of the entity list
        for j in gs.entityList:
            #draw a bcurve between the current entity and the other entities
            #this results in a line being drawn between each entity
            fillBCurve(i.x, i.y, j.x, j.y, 1, 3, 4, td)



    #replace every 0 tile with a 3 tile
    fillSwap(0, 3, td)
    #fill the main chamber with 0 tiles
    bucketFill(gs.entityList[0].x, gs.entityList[0].y, 3, 0, td)
    #this effectively choses a main chamber and fills all other chambers
    #that are not immediate peices of the region


    fillEdges(1, 0, 2, td)
    fillBoarder(1, td)


    #circle = hexCircle( int(xMax/2) , int(yMax/2) , int((xMax-1)/2))
    # for i in circle:
    #    td[i[0]][i[1]] = 3
    #    print(str(i))

    return gs
