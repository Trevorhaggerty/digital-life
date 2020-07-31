import numpy as np
from mathTools import *

# --------------------------------------------------------------------------------------------------------------


def hexDistance(x1, y1, x2, y2):
    return (abs((x1 - (y1 + (y1 & 1)) / 2) - (x2 - (y2 + (y2 & 1)) / 2)) + abs((-(x1 - (y1 + (y1 & 1)) / 2) - y1) - (-(x2 - (y2 + (y2 & 1)) / 2) - y2)) + abs((y1) - (y2))) / 2


def hex2t3(x, y):
    x1 = int(x - (y + (y & 1))/2)
    y1 = y
    z1 = -x1 - y1
    return [x1, y1, z1]


def hex3t2(x, y, z):
    x1 = int(x + (y + (y & 1))/2)
    return [x1, y]


def hexCircle(centerx, centery, radius, sampleRate):
    vectorBuffer = [0, 0]
    hexlist = []
    for i in range(sampleRate):
        hexlist.append([int(centerx + radius * (np.cos((lerp(0, 360, (i / sampleRate))) * np.pi / 180))) +
                        1, int(centery + radius * (np.sin((lerp(0, 360, (i / sampleRate))) * np.pi / 180)))])
        # print(str(hexlist))
    return hexlist


# -------------------------------------------------------------------------------------------------------------


def binNeighbor(x, y, target, terrainData):
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

    return counter
# ---------------------------------------------------------------------------------------


def tileTypeCount(target, terrainData):
    return terrainData.count(target)
