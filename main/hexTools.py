#libraries
import numpy as np
from mathTools import *

# ----------------------------------------------------------------------------------------
# hexDistance evaluates two EVEN R hex coordinates and returns the distance
#   it takes in:
#       - 2 EVEN R hex coordinates
#   and it returns:
#       - the distance between them
def hexDistance(x1, y1, x2, y2):
    return (abs((x1 - (y1 + (y1 & 1)) / 2) - (x2 - (y2 + (y2 & 1)) / 2)) + abs((-(x1 - (y1 + (y1 & 1)) / 2) - y1) - (-(x2 - (y2 + (y2 & 1)) / 2) - y2)) + abs((y1) - (y2))) / 2
# ----------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# hex2t3 takes an EVEN R coordinate and makes it a cube hex coordinate
#   it takes in:
#       - an EVEN R x y coordinate
#   and it returns:
#       - a cube coordinate
def hex2t3(x, y):
    x1 = int(x - (y + (y & 1))/2)
    y1 = y
    z1 = -x1 - y1
    return [x1, y1, z1]
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# hex3t2 takes a cube coordinate and makes it an EVEN R coordinate
#   it takes in:
#       - a cube coordinate
#   and it returns:
#       - an EVEN R coordinate
def hex3t2(x, y, z):
    x1 = int(x + (y + (y & 1))/2)
    return [x1, y]
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# roundHex3d rounds 3d float coordinates to the closest tile
#   it takes in:
#       - cube coordinates in float value
#   and it returns:
#       - cube coordinates in int values
def roundHex3d(x, y, z):
    #find the difference between the rounded values and the original values
    xd = abs( round(x) - x )
    yd = abs( round(y) - y )
    zd = abs( round(z) - z )
    #adjust the coordinate that is farthest in difference through
    if xd > yd and xd > zd:
        ox = -round(y)-round(z)
        oy = round(y)
        oz = round(z)
    elif yd > zd:
        ox = round(x)
        oy = -round(x)-round(z)
        oz = round(z)
    else:
        ox = round(x)
        oy = round(y)
        oz = -round(x)-round(y)
    #return adjusted values
    return [ox , oy , oz]
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# roundHex2d rounds 2d float coordinates to the closest tile
#   it takes in:
#       -2d coordinates in float values
#   and it returns:
#       -2d coordinates in int values
def roundHex2d(x, y):
    #convert 2d coordinates to 3d and round them
    hex3d = roundHex3d(hex2t3(x, y)[0], hex2t3(x, y)[1], hex2t3(x, y)[2])
    #return the rounded values converted to 2d
    return hex3t2(hex3d[0],hex3d[1],hex3d[2])
# ----------------------------------------------------------------------------------------







# ----------------------------------------------------------------------------------------
# hexCircle creates a list of EVEN R hex coordinates that fall on a circle with given 
#   center point, radius, and sampleRate ( the number of hexes in the returned list)
#   it takes in:
#       - center EVEN R coordinate
#       - radius in tile units
#       - sampleRate
#   it returns:
#       - a list of hexs that are on the circle
def hexCircle(centerx, centery, radius, sampleRate):
    #create a list to hold the hex coordinates
    hexlist = []
    #itterate through sampleRate (limits number of returned hexs)
    for i in range(sampleRate):
        #if the hex falls on the circle append it to the hexlist
        hexlist.append([int(centerx + radius * (np.cos((lerp(0, 360, (i / sampleRate))) * np.pi / 180))) +
                        1, int(centery + radius * (np.sin((lerp(0, 360, (i / sampleRate))) * np.pi / 180)))])
        # print(str(hexlist))
    return hexlist
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# binNeighbor take an EVEN R coordinate and a vector telling if a neighbor is of target tile type
#   it takes in:
#       - EVEN R x y coordinate
#       - the target tile type
#       - the terrain data to analyze
#   and it returns:
#       - vector of binary values representing neighbors with target tile
def binNeighbor(x, y, target, terrainData):
    #create vector of size 6 with all zeros
    counter = [0, 0, 0, 0, 0, 0]

    if (y % 2 != 0 and x < len(terrainData) - 1 and y < len(terrainData[0]) - 1 and x > 0 and y > 0):
        if (terrainData[x - 1][y - 1] == target):
            counter[0] += 1
        if (terrainData[x - 0][y - 1] == target):
            counter[1] += 1
        if (terrainData[x + 1][y + 0] == target):
            counter[2] += 1
        if (terrainData[x + 0][y + 1] == target):
            counter[3] += 1
        if (terrainData[x - 1][y + 1] == target):
            counter[4] += 1
        if (terrainData[x - 1][y + 0] == target):
            counter[5] += 1

    elif (y % 2 == 0 and x < len(terrainData) - 1 and y < len(terrainData[0]) - 1 and x > 0 and y > 0):
        if (terrainData[x + 0][y - 1] == target):
            counter[0] += 1
        if (terrainData[x + 1][y - 1] == target):
            counter[1] += 1
        if (terrainData[x + 1][y + 0] == target):
            counter[2] += 1
        if (terrainData[x + 1][y + 1] == target):
            counter[3] += 1
        if (terrainData[x + 0][y + 1] == target):
            counter[4] += 1
        if (terrainData[x - 1][y + 0] == target):
            counter[5] += 1
    #if the function completes return counter vector
    return counter
# ---------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------
# tileTypeCount counts the amount of a specific tile are present on the board
#   it takes in:
#       - target tile
#       - the terrain data to analyze
#   and it returns:
#       - the number of target tiles present
def tileTypeCount(target, terrainData):
    return terrainData.count(target)
