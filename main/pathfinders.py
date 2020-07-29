
import numpy as np
from hexTools import *
from terrainGenerator import *
from printingHandler import *
from entities import *



class sTile:
    def __init__(self, x, y, passablity):
        self.x = x
        self.y = y
        self.passablity = passablity
        self.whereParentDirection = -1
        self.knownValue = None

    def info(self):
        return str(self.x) + ' , ' + str(self.y) + ' , ' + str(self.passablity) + ' , ' + str(self.whereParentDirection) + ' , ' + str(self.knownValue)

class cursorC:
    #all entities will have an x,y location and an type for location in the datastructure
    def __init__(self, x, y, path):
        #fill the x
        self.x = x
        #fill the y
        self.y = y

        self.path = path



def printSTileMap(sTileMap, home, goal, cursor):
    clearScreen()
    for y in range(len(sTileMap[0])):
        if y%2 == 0 :
            print('  ', end = '')
        for x in range(len(sTileMap)):
            if x == home[0] and y == home[1]:
                print("HOM", end = ' ')
            elif x == goal[0] and y == goal[1]:
                print("GOL", end=' ')
            elif x == cursor.x and y == cursor.y:
                print("CUR", end=' ')
            elif sTileMap[x][y].whereParentDirection == -1:
                if sTileMap[x][y].passablity == True:         
                    print('   ', end = ' ')
                else:
                    print('xxx', end = ' ')
            else:
                print(' ' + str(sTileMap[x][y].whereParentDirection), end='  ')
        print()

def stNeighbor(x, y, target, sTileMap):
    counter = [0, 0, 0, 0, 0, 0]
    if (y % 2 != 0 and x < len(sTileMap) - 1 and y < len(sTileMap[0]) - 1 and x > 0 and y > 0):
        if (sTileMap[x - 1][y - 1].knownValue == target):
            counter[0] += 1
        if (sTileMap[x - 0][y - 1].knownValue == target):
            counter[1] += 1
        if (sTileMap[x + 1][y + 0].knownValue == target):
            counter[2] += 1
        if (sTileMap[x + 0][y + 1].knownValue == target):
            counter[3] += 1
        if (sTileMap[x - 1][y + 1].knownValue == target):
            counter[4] += 1
        if (sTileMap[x - 1][y + 0].knownValue == target):
            counter[5] += 1

    elif (y % 2 == 0 and x < len(sTileMap) - 1 and y < len(sTileMap[0]) - 1 and x > 0 and y > 0):
        if (sTileMap[x + 0][y - 1].knownValue == target):
            counter[0] += 1
        if (sTileMap[x + 1][y - 1].knownValue == target):
            counter[1] += 1
        if (sTileMap[x + 1][y + 0].knownValue == target):
            counter[2] += 1
        if (sTileMap[x + 1][y + 1].knownValue == target):
            counter[3] += 1
        if (sTileMap[x + 0][y + 1].knownValue == target):
            counter[4] += 1
        if (sTileMap[x - 1][y + 0].knownValue == target):
            counter[5] += 1

    return counter


def iteratePathfind(currentStep, sTileMap):  # if a is touching any b make a become c
    for y in range(len(sTileMap[0])):
        for x in range(len(sTileMap)):
            
            detectedVector = stNeighbor(x, y, currentStep-1, sTileMap)
            edgesDetected = sum(detectedVector)

            whereParentvector = [detectedVector[3],detectedVector[4],detectedVector[5],detectedVector[0],detectedVector[1],detectedVector[2]]
            parentDirection = np.argmax(whereParentvector)

            #parentDirection = np.argmax(detectedVector)

            if sTileMap[x][y].passablity == True and edgesDetected > 0 and sTileMap[x][y].knownValue == None:
                
                sTileMap[x][y].knownValue = currentStep
                sTileMap[x][y].whereParentDirection = parentDirection


    return sTileMap


def movesTileCursor(cursor, sTileMap):
    cursor.path.insert(0,sTileMap[cursor.x][cursor.y].whereParentDirection)
    if cursor.y % 2 != 0:
        if cursor.path[0] == 3:
            cursor.x -= 1
            cursor.y -= 1
            return 1
        if cursor.path[0] == 4:
            cursor.x += 0
            cursor.y -= 1
            return 1
        if cursor.path[0] == 5:
            cursor.x += 1
            cursor.y += 0
            return 1
        if cursor.path[0] == 0:
            cursor.x += 0
            cursor.y += 1
            return 1
        if cursor.path[0] == 1:
            cursor.x -= 1
            cursor.y += 1
            return 1
        if cursor.path[0] == 2:
            cursor.x -= 1
            cursor.y += 0
            return 1
    elif cursor.y % 2 == 0:
        if cursor.path[0] == 3:
            cursor.x += 0
            cursor.y -= 1
            return 1
        if cursor.path[0] == 4:
            cursor.x += 1
            cursor.y -= 1
            return 1
        if cursor.path[0] == 5:
            cursor.x += 1
            cursor.y += 0
            return 1
        if cursor.path[0] == 0:
            cursor.x += 1
            cursor.y += 1
            return 1
        if cursor.path[0] == 1:
            cursor.x += 0
            cursor.y += 1
            return 1
        if cursor.path[0] == 2:
            cursor.x -= 1
            cursor.y += 0
            return 1
    else:
        return -1            #print('the way is blocked')

# ---------------------------------------------------------------------------------------
# starting and ending 2d locations with a 2 evenr hexagon binmap
def pathFinding(givenMap, passableTile, home, goal, outtype = 0): #outtype 0 = is directions # outtype 1 is the tiles x,y data
    sTileMap = [[0 for x in range(len(givenMap[0]))]
                for x in range(len(givenMap))]
    for j in range(len(givenMap[0])):
        for i in range(len(givenMap)):
            if givenMap[i][j] == passableTile:
                sTileMap[i][j] = sTile(i, j, True)
            else:
                sTileMap[i][j] = sTile(i, j, False)
            #print(sTileMap[i][j].info())
    cursor = cursorC(goal[0],goal[1],[])
    sTileMap[home[0]][home[1]].knownValue = 0
    print(sTileMap[home[0]][home[1]].info())
    currentStep = 0
    while sTileMap[goal[0]][goal[1]].knownValue == None:
        sTileMap = iteratePathfind(currentStep, sTileMap)
        currentStep +=1
        if currentStep > 100:
            break
        printSTileMap(sTileMap, home, goal, cursor)
    print(str(currentStep))
    sTileMap = iteratePathfind(currentStep, sTileMap)
    print(sTileMap[goal[0]][goal[1]].info())
    pathxy = []
    count = 0
    while cursor.x != home[0] or cursor.y != home[1]:
        movesTileCursor(cursor, sTileMap)

        if outtype == 1:
            pathxy.insert(0,[cursor.x,cursor.y])
        if count > sTileMap[goal[0]][goal[1]].knownValue:
            break
        count += 1
        printSTileMap(sTileMap, home, goal, cursor)
    if outtype == 1:
        return pathxy
    return cursor.path
