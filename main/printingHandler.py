import random
import sys
from os import system, name 

def clearScreen():
    if name == 'nt': 
	    _ = system('cls')
    else: 
	    _ = system('clear') 

def colorize(text,forground, background):
    text = (u"\033[0;" + str(((forground) % 8) + 30) + ";" + str(((background) % 8) + 40) + ";99"  + "m" + str(text)) + '\033[0m'
    return text

def printGameSpace(gameSpace) :
    clearScreen()
    vertCaps = ("@-" + "____" * gameSpace.xMax + "-@")
    for y in range(gameSpace.yMax) :
        for x in range(gameSpace.xMax) :
            if y == 0 and x == 0:
                print (colorize( vertCaps ,2,0))
            if x == 0:
                if y % 2 != 0:
                    print (colorize('|',2,0), end = "")
                else:
                    print (colorize('|  ',2,0), end = "")
            print (colorize(' ',2,0), end = "")
            a = False
            for z in gameSpace.entityList :
                if z.x == x and z.y == y :
                    print (colorize(z.appearance[0],z.appearance[1],z.appearance[2]), end = "")
                    a = True
                    break
            if a == False :
                if gameSpace.terrainData[x][y] == 0 :
                        print (colorize(' . ',7,0), end = "")
                #
                elif gameSpace.terrainData[x][y] == 1 :
                    print (colorize('░░░',7,0), end = "")
                elif gameSpace.terrainData[x][y] == 2 :
                    print (colorize('▒▒▒',7,0), end = "")        
                elif gameSpace.terrainData[x][y] == 3:
                    print (colorize('▓▓▓',7,0), end = "")
        if y % 2 != 0:
            print (colorize('  |',2,0))
        else :
            print (colorize('|',2,0))
        if (y == gameSpace.yMax-1 and x == gameSpace.xMax-1):
            print (colorize( vertCaps ,2,0))
