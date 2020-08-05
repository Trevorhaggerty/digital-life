import random
import sys
from os import system, name 
import time
from animations import *


#global string that acts like an array of characters with the index as the value
#grayscalewtb goes from the most space filling characters to the least
grayscalewtb = "$@B%8&WM#oahkbdpqwmZO0QLYXCJUzcvunxrjft/\|()1{}[]?<>i!lI;:+~,.- "
#grayscalebtw goes from the least space filling characters to the most
grayscalebtw = ''.join(reversed(grayscalewtb))

#clearScreen is a screen clearing function
def clearScreen():
    #if the system is windows use cls
    if name == 'nt': 
	    _ = system('cls')
    #if its a linux system use clear
    else: 
	    _ = system('clear') 
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# colorize is a function that takes in a string and adds unicode escape colors
#   it takes in:
#       - a string to be modified
#       - the color of the text
#       - the color of the backround
#   and it returns:
#       - a string with color information
def colorize(text,forground, background):
    return (u"\033[0;" + str(((forground) % 8) + 30) + ";" + str(((background) % 8) + 40) + ";99"  + "m" + str(text)) + '\033[0m'
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# printGameSpace prints the current state of the given gamespace and waits for
#   a period of time. it scans left to right top to bottom. its meant to act ike an ascii shader.
#   it takes in:
#       - the gameSpace object to print (object)
#       - the focus of the screen   [(int),(int)]
#       - the dimensions of the veiwport [(int),(int)]
#       - the delay after print (float)
#   it returns:
#       - 
def printGameSpace(gs, centerPointVector, screenSizeVector, delay) :
    #find the minimum and maximum x,y values for scanning to screen
        #use an if statement to check if its in the confines of the map
        #if so adjust the min or max value
    xMin = int(centerPointVector[0] - (screenSizeVector[0] / 2))
    if xMin < 0:
        xMin = 0
    xMax = int(centerPointVector[0] + (screenSizeVector[0] / 2))
    if xMax > gs.xMax:
        xMax = gs.xMax
    yMin = int(centerPointVector[1] - (screenSizeVector[1] / 2))
    if yMin < 0:
        yMin = 0
    yMax = int(centerPointVector[1] + (screenSizeVector[1] / 2))
    if yMax > gs.yMax:
        yMax = gs.yMax
    #clear the screen to prepare for a screen writing
    clearScreen()
    #save the character design for the top and bottom of the screens frame
    vertCaps = ("@-" + "____" *(xMax - xMin) + "-@")
    #itterate through the y axis
    for y in range(yMin, yMax):
        #itterate throught the x axis
        for x in range(xMin, xMax):
            # if this is the first itteration of the scan
            if y == yMin and x == xMin:
                #print the top cap
                print (colorize( vertCaps ,2,0))
            #if this is a new line of the scan
            if x == xMin:
                #if this is on an odd row
                if y % 2 != 0:
                    #print left border with no offset
                    print (colorize('| ',2,0), end = "")
                #if this is on an even row
                else:
                    #print left with a 2 char offset
                    print (colorize('|   ',2,0), end = "")
            #put a gap between the tiles on the same row 
            print (colorize(' ',2,0), end = "")
            #bool for determinining if an entity has been drawn
            a = False
            #itterate through each entity
            for z in gs.entityList :
                #if the entities x and y location match the scan x and y
                if z.x == x and z.y == y :
                    #if the entities appearance is 'bat' 
                    if z.appearance[0] == 'goblin':
                        #save the current frame of the goblin animation as frame
                        frame = goblinAnim[gs.screenCount % len(goblinAnim)]
                        #print the frame with appropriate colors
                        print (colorize(frame,z.appearance[1],z.appearance[2]), end = "")
                    elif z.appearance[0] == 'food':
                        #save the current frame of the food animation as frame
                        frame = foodAnim[gs.screenCount % len(foodAnim)]
                        #print the frame with appropriate colors
                        print (colorize(frame,z.appearance[1],z.appearance[2]), end = "")
                    elif z.appearance[0] == 'bat':
                        #save the current frame of the bat animation as frame
                        frame = batAnim[gs.screenCount % len(batAnim)]
                        #print the frame with appropriate colors
                        print (colorize(frame,z.appearance[1],z.appearance[2]), end = "")
                    else:
                        #print the entities forground characterset, forground color, and backround color
                        print (colorize(z.appearance[0],z.appearance[1],z.appearance[2]), end = "")


                    #set the entity draw bool to true
                    a = True
                    #break from the for loop as to not draw multiple times for no reason
                    break
            #if there were no entities to draw at the location
            if a == False :
                #is this an 'idea' object/tile
                if gs.terrainData[x][y] == -2:
                    #print static
                   print (colorize((grayscalebtw[random.randint(0,6)] + grayscalebtw[random.randint(0,60)] + grayscalebtw[random.randint(0,60)]),7,0), end = "") 
                #if this is an actual tile
                else:
                    #print the tile based on its saved value and the index it correlates to
                    print (colorize((grayscalebtw[((gs.terrainData[x][y])%len(grayscalebtw))]*3),7,0), end = "")

        #if the row is odd
        if y % 2 != 0:
            #print a spacer and the right border
            print (colorize('  |',2,0))
        #if the row is even
        else :
            #print right border
            print (colorize('|',2,0))
        
        #if this is the last scans last inspection
        if (y == yMax-1 and x == xMax-1):
            #print the bottom cap
            print (colorize( vertCaps ,2,0))
    # after full scan and print wait for the given value of seconds
    time.sleep(delay)   
    #itterate the screen counter
    gs.screenCount +=1
    