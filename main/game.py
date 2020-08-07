# game.py contains the main function and gameloop

# libraries
import numpy as np
import sys
import random
import datetime

# local import
from terrainGenerator import *
from printingHandler import *
from inputHandler import *
from eventLog import *
from kmean import *
from nnode import *
from hexTools import *

# create the log handling object
logger = eventLog(
    'Goblin Tentacles Python : monster simulation', '0.2', 5, True)

# start the game/simulation
def main():

    # save the time the game began for later use
    startTime = time.time()
    # update currentTime
    currentTime = (time.time() - startTime)

    # begin the game with a given time limit in seconds
    while currentTime < 5000:

        # use the create terrain function to produce the disired gameSpace object
        # createTerrain(x size, y size, random seed, 'spaciousness', presence of water)
        gs = createTerrain(32, 32, datetime.datetime.now(), 13, False)
        # log the success of the function
        logger.logEvent('terrain generated', 5)
        # save the list of produced entities into a more digestable var
        entl = gs.entityList

        # update currentTime
        currentTime = (time.time() - startTime)
        # set the new sessions end condition to false
        gameOver = False

        # begin session loop with bool end condition
        while gameOver == False:

            # update the current time
            currentTime = (time.time() - startTime)
            # display the current sessions tick and time
            logger.logEvent('gs.tick:' + str(gs.tick) + ', ' +
                            str(currentTime) + 'sec from program start', 0)

            
            for i in range(18):
                # use the printingHandler to print the games current state
                printGameSpace(gs, [int(gs.xMax/2), int(gs.yMax/2)], [gs.xMax,gs.yMax], 0.05)

            # create holder to count the number of entities on the board
            count = 0
            # create int to hold wether an entity should be deleted from the array
            j = -2
            # iterate through the list of entities
            for i in range(len(entl)):
                # call each of the entities update function
                entl[i].update(gs)
                # if the HP of the entity falls to or under 0
                if entl[i].HP <= 0:
                    # save the index of the entity
                    j = i
                # if the entities type is 'monster' iterate count
                if entl[i].type == 'monster':
                    count += 1
            # if the j is a valid positive index
            if j >= 0:
                #check to see if this is the last monster
                if count >= 2:
                    # remove the entity from the list
                    del entl[j]

            # if theRE CAN BE ONLY 1!!!
            if count <= 1:
                # iterate through the entity list
                for ent in entl:
                    # save and print the monsters information
                    ent.info()
                # print the current game state at end
                    printGameSpace(gs, [int(gs.xMax/2), int(gs.yMax/2)], [gs.xMax,gs.yMax], 0.05)
                # set the sessions end status to true
                gameOver = True


            # after the number of epochs is above a given value
            if gs.tick > 10000:

                # iterate through the entity list
                for ent in entl:
                    # save and print the monsters information
                    ent.info()
                # print the current game state at end
                    printGameSpace(gs, [int(gs.xMax/2), int(gs.yMax/2)], [gs.xMax,gs.yMax], 0.05)
                # set the sessions end status to true
                gameOver = True

            # iterate the game tick / epoch
            gs.tick += 1

            # when a certain number of epochs pass
            if gs.tick % 5001 == 0:
                # request user input, and if the user enters 'x'
                if requestContinue() == 'x':
                    # iterate through the entity list
                    for ent in entl:
                        # save and print the monsters information
                        ent.info()
                    # print the current game state at end
                    printGameSpace(gs, [int(gs.xMax/2), int(gs.yMax/2)], [gs.xMax,gs.yMax], 0.05)
                    # set the sessions end status to true
                    gameOver = True