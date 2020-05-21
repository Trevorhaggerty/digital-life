import random
import sys


def colorize(text,forground, background):
    text = (u"\033[0;" + str(((forground) % 8) + 30) + ";" + str(((background) % 8) + 40) + ";99"  + "m" + str(text)) + '\033[0m'
    return text


def printGameSpace(gameSpace, entityList, xrange, yrange) :
    print(colorize('',2,0))
    for y in range(yrange) :
        for x in range(xrange) :
            if y == 0 and x == 0:
                print ("@" + "__" * xrange + "@")
            if x == 0:
                print ("|", end = "")
            a = False
            for z in entityList :
                if z.x == x and z.y == y :
                    print (colorize(z.appearance[0],z.appearance[1],z.appearance[2]), end = "")
                    print (colorize('',2,0), end = "")
                    a = True
                    break
            if a == False :
                print (gameSpace[x][y], end = "")
        print ("|" , end = "")
        print ('')
        if (y == yrange-1 and x == xrange-1):
            print ("@" + "__" * xrange + "@")

def printGraph(gameSpace, pointsList, xrange, yrange) :
    print(colorize('',2,0))
    for y1 in range(yrange) :
        y = yrange - y1 -1
        for x in range(xrange) :
            if y == 0 and x == 0:
                print ("@" + "__" * xrange + "@")
            if x == 0:
                print ("|", end = "")
            a = False
            for z in range(len(pointsList[0])) :
                if pointsList[1][z] == y and pointsList[0][z] == x:
                    print (colorize( "██", 1 , 0), end = "")
                    a = True
                    break
            if a == False :
                print (gameSpace[x][y], end = "")
        print ("|" , end = "")
        print ('')
        if (y == yrange-1 and x == xrange-1):
            print ("@" + "__" * xrange + "@")

