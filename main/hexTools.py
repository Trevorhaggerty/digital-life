#--------------------------------------------------------------------------------------------------------------
def hexDistance(x1, y1, x2, y2):
    return (abs((x1 - (y1 + (y1&1)) / 2) - (x2 - (y2 + (y2&1)) / 2)) + abs((-(x1 - (y1 + (y1&1)) / 2) - y1) - (-(x2 - (y2 + (y2&1)) / 2) - y2) ) + abs((y1) - (y2))) / 2

def hex2t3(x,y):
    x1 = int(x - (y + (y&1))/2)
    y1 = y
    z1 = -x1 - y1    
    return [x1,y1,z1]




#-------------------------------------------------------------------------------------------------------------
def binNeighbor(x, y, target, gameSpace) :
    counter = [0,0,0,0,0,0]
    if (y % 2 != 0 and x < gameSpace.xMax - 1 and y < gameSpace.yMax - 1 and x > 0 and y > 0):
    	if (gameSpace.terrainData[x - 1][y - 1] == target) :
            counter[0]+= 1
    	if (gameSpace.terrainData[x - 0][y - 1] == target) :
            counter[1]+= 1
    	if (gameSpace.terrainData[x + 1][y + 0] == target) :
            counter[2]+= 1
    	if (gameSpace.terrainData[x + 0][y + 1] == target) :
            counter[3]+= 1
    	if (gameSpace.terrainData[x - 1][y + 1] == target) :
            counter[4]+= 1
    	if (gameSpace.terrainData[x - 1][y + 0] == target) :
            counter[5]+= 1

    elif (y % 2 == 0 and x < gameSpace.xMax - 1 and y < gameSpace.yMax - 1 and x > 0 and y > 0) :
    	if (gameSpace.terrainData[x + 0][y - 1] == target) : 
            counter[0]+=1 
    	if (gameSpace.terrainData[x + 1][y - 1] == target) : 
            counter[1]+=1
    	if (gameSpace.terrainData[x + 1][y + 0] == target) : 
            counter[2]+=1
    	if (gameSpace.terrainData[x + 1][y + 1] == target) : 
            counter[3]+=1
    	if (gameSpace.terrainData[x + 0][y + 1] == target) : 
            counter[4]+=1
    	if (gameSpace.terrainData[x - 1][y + 0] == target) : 
            counter[5]+=1

    return counter
#---------------------------------------------------------------------------------------
def tileTypeCount(tileType, gameSpace):
    return gameSpace.terrainData.count(tileType)
