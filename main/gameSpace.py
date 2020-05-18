import random
import sys


def colorize(text,forground, background):
    text = (u"\033[0;" + str(((forground) % 8) + 30) + ";" + str(((background) % 8) + 40) + ";99"  + "m" + str(text)) + '\033[0m'
    return text


def printGameSpace(gameSpace, entityList, xrange, yrange) :
    print(colorize('',2,0))
    infoString = ''
    infoCount = 0
    for y in range(yrange) :
        for x in range(xrange) :
            if y == 0 and x == 0:
                print ("__" * xrange)
            if x == 0:
                print ("|", end = "")
            
            
            a = False
            for z in entityList :
                if z.x == x and z.y == y :

                    print (colorize(z.appearance[0],z.appearance[1],z.appearance[2]), end = "")
                    print (colorize('',2,0), end = "")
                    infoString += z.info()  # <<<<<<<<-----------------------------------------------------------------------------
                    infoCount += 1
                    a = True
                    break
            if a == False :
                print (gameSpace[x][y], end = "")
        print ("|" , end = "")
        print (str(infoString), end = "")
        infoCount = 0
        infoString = ''
        print ('')
        if (y == yrange-1 and x == xrange-1):
            print ("|" + "__" * xrange + "|")




#Background White: \u001b[47m
#Background Black: \u001b[40m
#Background Red: \u001b[41m
#Background Green: \u001b[42m
#Background Yellow: \u001b[43m
#Background Blue: \u001b[44m
#Background Magenta: \u001b[45m
#Background Cyan: \u001b[46m
#Background Bright Black: \u001b[40;1m
#Background Bright Red: \u001b[41;1m
#Background Bright Green: \u001b[42;1m
#Background Bright Yellow: \u001b[43;1m
#Background Bright Blue: \u001b[44;1m
#Background Bright Magenta: \u001b[45;1m
#Background Bright Cyan: \u001b[46;1m
#Background Bright White: \u001b[47;1m
#sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
#sys.stdout.write(u"\u001b[48;5;" + code + "m " + code.ljust(4))