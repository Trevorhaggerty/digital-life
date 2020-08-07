#libraries
import numpy as np
import sys

#local imports
from nnode import *
from ffnnetwork import *
from terrainGenerator import *
from hexTools import *
from mathTools import *
from printingHandler import *
from gameSpace import *
from pathfinders import *


# ----------------------------------------------------------------------------------------
# entity is the parent object to all other objects that hold all of the data pertaining to
#   the entities that inhabit the gameSpace. The base for other entity like classes
#   it takes in:
#       - the x and y coordinates the entity exists at
#       - an ID for keeping track of individual entities
#   it contains:
#       - the x and y coordinates the entity exists at
#       - an ID for keeping track of individual entities
#       - the move() function which modifies x y coordinates of the entity it is called in
#           so that they move correctly on an EVEN R Hexagonal grid
class entity :
    #all entities will have an x,y location and an type for location in the datastructure
    def __init__(self, x, y, ID):
        self.x = x
        self.y = y
        self.ID = ID
    # ------------------------------------------------------------------------------------
    # move uses the binNeighbor function to find if an entity is capable of movement in an
    #   input direction on a given gamespace and implement the correct modifications to the
    #   x y coordinates of the entity that it is called within.
    #   it takes in:
    #       - the disired direction of movement as an int 0-5 inclusive
    #       - the gameSpace this takes place in
    #   and it returns:
    #       - (1) for success and (-1) for failure
    def move(self, direction, gs):
        #check the neighbor in the intended direction to see if its a 0
        if binNeighbor(self.x, self.y, 0, gs.terrainData)[direction] == 1:
            #if entity is on an odd tile
            if self.y % 2 != 0:
                if direction == 0:
                    self.x -= 1
                    self.y -= 1
                    return 1
                if direction == 1:
                    self.x += 0 
                    self.y -= 1
                    return 1
                if direction == 2:
                    self.x += 1
                    self.y += 0
                    return 1
                if direction == 3:
                    self.x += 0
                    self.y += 1
                    return 1
                if direction == 4:
                    self.x -= 1
                    self.y += 1
                    return 1
                if direction == 5:
                    self.x -= 1
                    self.y += 0
                    return 1
            #if the entity is on an even tile
            elif self.y % 2 == 0:
                if direction == 0:
                    self.x += 0
                    self.y -= 1
                    return 1
                if direction == 1:
                    self.x += 1
                    self.y -= 1
                    return 1
                if direction == 2:
                    self.x += 1
                    self.y += 0
                    return 1
                if direction == 3:
                    self.x += 1
                    self.y += 1
                    return 1
                if direction == 4:
                    self.x += 0
                    self.y += 1
                    return 1
                if direction == 5:
                    self.x -= 1
                    self.y += 0
                    return 1
        else:
        #if movment failed return -1
            return -1           
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# redolent is a child of the entity class. used for a place holder of an entity in the 
#   gameSpace in an entities imaginationSpace. Just the appearance and location
#   of an entity are stored for use in path finding and eventually plan building.
#   Essentially the place holder for the "idea" an entity has of another
#   it takes in:
#       - the x and y coordinates the entity exists at (int) (int)
#       - the appearance the entity will retain ([str,int,int])
#       - an ID for keeping track of individual entities (uuid4)
#   it contains:
#       - the x and y coordinates the entity exists at (int) (int)
#       - an ID for keeping track of individual entities (uuid4)
#       - the type of entity that it is (str)
#       - the appearance the entity will retain ([str,int,int])
#       - HP of the redolent (int)
#       - the age of the entity (int)
class redolent(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, appearance, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        self.ID = ID
        self.type = 'redolent'
        self.appearance = appearance
        self.HP = 1
        self.age = 0


# ----------------------------------------------------------------------------------------
# food is a child of the entity class. This entity acts as a source of 'food', giving the
#   entity who 'consumed' it an increase in HP, then the food teleports to a random
#   location on the gamespace ( given that the location is an open tile)
#   it takes in:
#       - the x and y coordinates the entity exists at (int) (int)
#       - an ID for keeping track of individual entities (uuid4)
#       - HP the food pellet rewards (int)
#   it contains:
#       - the x and y coordinates the entity exists at (int) (int)
#       - an ID for keeping track of individual entities (uuid4)
#       - the type of entity that it is (str)
#       - the appearance the entity will retain ([str,int,int])
#       - HP the food pellet rewards (int)
#       - the age of the entity (int)
#       - the update() function which checks if a monster entity is in contact with it,
#           and if it is, add HP to the entity and call the teleport function.
#       - the teleport() function which when called loops, choosing a random coordinate
#           and checking to see if it is an open tile. If the tile is open the food's
#           x y coordinates are modified to that locations
class food(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, HP, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        self.ID = ID
        self.type = 'food'
        self.appearance = ['food', 2, 0]
        self.HP = HP
        self.age = 0


    # ------------------------------------------------------------------------------------
    #update checks wether a monster entity is on the same tile as the food, if it is add
    #   the same amount of HP the food has to the entity and call the teleport function.
    #   if the food has not been touched in 100 epochs call the teleport function.
    #   it takes in:
    #       - the gameSpace
    def update(self, gs):
        #create int to hold the index of the possible target entitiy    
        j = 0
        #scan the entity list for any entities standing at the same location as the 
            #food and that the entity is a 'monster' type.
        for i in gs.entityList:
            if i.x == self.x and i.y == self.y and i.type == 'monster':
                #call the teleport function
                self.teleport(gs)
                #heal the cooresponding monster
                gs.entityList[j].HP += self.HP
            #iterate the index counting variable
            j += 1
        #iterate the age
        self.age += 1
        #if the age is over 100
        if self.age >= 100:
            #call the teleport function
            self.teleport(gs)
        #if all goes as planned return 0
        return 0

    #----------------------------------------------------------------------------------------
    #teleport randomizes x and y coordinates of the entity it is called in. The gamespace is 
    #   refrenced to ensure that the locations chosen arent rediculus like in a wall or off a
    #   cliff.
    #   it takes in:
    #       - the gameSpace
    #   it returns:
    def teleport(self, gs):
        #create boolean to control while loop
        looking = True
        while looking:
            #choose a random x and y location that is within the confines of the local gamespace
            x , y = np.random.randint(4,gs.xMax - 3), np.random.randint(4,gs.xMax - 3)
            # determine if the location is empty
            if gs.terrainData[x][y] == 0:
                #set the entities location to the chosen coordinates
                self.x = x
                self.y = y
                #set the age of the entity back to 0
                self.age = 0
                #set the end condition for the while loop
                looking = False

    #--------------------------------------------------------------------------------------------
    #info <----- empty place holder function for entity generalizations
    def info(self):
        return 0
# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# monster is a child of the entity class. This entity acts as an agent of the forward feeding
#   neural network that controls it. It 'forages' by wandering the gameSpace and collecting 
#   food. The monster entities HP decrements ater a given time and if the monster entity goes
#   too long without food it is deleted from the gameMap, thus dying.
#   it takes in:
#       - the x and y coordinates the entity exists at (int) (int)
#       - the DNA a list of varius types that determine the morphology and behavior of the entity
#       - an ID for keeping track of individual entities (uuid4)
#   it contains:
#       - the x and y coordinates the entity exists at (int) (int)
#       - an ID for keeping track of individual entities (uuid4)
#       - the type of entity that it is (str)
#       - the entities DNA list
#       - the appearance the entity will retain ([str,int,int])
#       - HP the health of the entity (int)
#       - the age of the entity (int)
#       - the senseArray
#       - the brain which is an instance of the ffnnetwork class who's dimensions and learningrates
#           Are determined by the monster entities DNA list
#       - the maturity is an int that acts as a threshold on age to determine if the cell is mature
#       - the costList is a memory of the past cost for summation to evaluate the current cost
#       - the cost is the measure of how wrong the monster's brain was 
#       - the foodTargetVector hold the location of the monster entities target food peice
#       - the pathfound array which contains the optimizes path
#       - the optimizeVector 
#       - the imaginationSpace which is an instance of the gameSpace object used to save and evaluate
#           the data that the monster collects and use that space for the planning and optimization.
#           This space remains empty until the 'monster' 'sees' the tile, so as to limit the possible
#           'correct answer' for the backpropagation of the brain to something that could be gleened
#           from the same previously experianced data
#       - the homeostasis() function which manages the decay of HP and age 
#       - the sense() function which creates the senseArray from gameSpace data
#       - the update() function which 
#       - the update() function which 
class monster(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, DNA, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        self.type = 'monster'
        self.DNA = DNA
        self.appearance = ['goblin', self.DNA[1], 0 ]
        self.HP = 15
        self.age = 0
        self.HPOld = self.HP
        self.senseArray = []
        self.brain = ffnnetwork(31,self.DNA[2],self.DNA[3],6,self.DNA[4])
        self.maturity = 1000
        self.costList = [1]
        self.cost = 1
        self.foodTargetVector = []
        self.pathfound = []
        self.optimizeVector = []
        self.imaginationSpace = gameSpace(32, 32)
        for j in range(len(self.imaginationSpace.terrainData[0])):
            for i in range(len(self.imaginationSpace.terrainData)):
                self.imaginationSpace.terrainData[i][j] = 0
    

    # ------------------------------------------------------------------------------
    # homeostasis() evaluates and increments the age. If the age has reached a specific threshold
    #   decrement the HP.
    def homeostasis(self):
        #if the age has hit a multiple of 25 
        if self.age % 25 == 0 and self.age > 0:
            #decrement hp
            self.HP -= 1
            #limit the HP to 15 and no higher
        if self.HP > 15:
            self.HP = 15

        #increment age
        self.age +=1
        return 0
    

    #------------------------------------------------------------------------------------------------
    #sense is a function that collects various types of information from the gameSpace and uses
    #   the obtained information to create a vector to act as the 'monster' entities senses.
    #   The collection of senses are as follows
    #       -touch (is there a wall near the monster)       (6 bin slots)
    #       -hearing (what of the 6 directions is the food) (6 bin slots)
    #       -HP sense (how healthy is the monster)          (4 bin slots)
    #       -sight (radial vision, distance to obsticle)    (15 int slots)
    #   the vectors are concatonated together and are the inputs to the brain with the senseArray.
    #   it takes in:
    #       - the gameSpace
    def sense(self, gs):

        #---------feeling-----------------

        #the feeling section of the senseArray simply does a check for tiles that are empty
        #   if the tile is not empty return a 1 (the logical opposite of the binNeighbor result)
        feeling = np.logical_not(binNeighbor(self.x, self.y, 0, gs.terrainData)).astype(int) 
        
        #---------hearing-----------------

        #create 2 empty lists to act as buffers
        vectorBuffer1 = []
        vectorBuffer2 = []
        #check through the list of enities
        for i in range(len(gs.entityList)):
            #if the entity is the type food
            if gs.entityList[i].type == 'food':
                #record its distance from the 'monster' entity
                vectorBuffer1.append(hexDistance(self.x,self.y, gs.entityList[i].x, gs.entityList[i].y))
                #save the index of the food entity in question
                vectorBuffer2.append(i)
        # find the index of the entity with the smallest distance to the 'monster'
        intBuffer = vectorBuffer2[np.argmin(vectorBuffer1)]
        #clear the buffers
        vectorBuffer1 = []
        vectorBuffer2 = []
        #set the foodTargetVector to the coordinates of the closest food entity
        self.foodTargetVector = [gs.entityList[intBuffer].x,gs.entityList[intBuffer].y]
        #fill buffer 1 with the cube location of the food
        vectorBuffer1 = hex2t3(gs.entityList[intBuffer].x,gs.entityList[intBuffer].y)
        #fill bodyXYZ with the cube location of the 'monster'
        bodyXYZ = hex2t3(self.x, self.y)
        #find the difference between these vectors
        vectorBuffer3 = np.subtract(vectorBuffer1, bodyXYZ)
        #absolute value the result to get the cube magnitudes
        vectorBuffer1 = np.absolute(vectorBuffer3)
        #find the index (and thus cubic direction) of the smallest magnitude
        intBuffer = np.argmin(vectorBuffer1)
        #use the integer found to create a vector that expresses to the NN what direction the food is in
        if intBuffer == 0:
            if vectorBuffer3[1] >= 0 and vectorBuffer3[2] <= 0:
                #the food is SE
                hearing = [0,0,0,1,0,0]
            else :
                #the food is NW
                hearing = [1,0,0,0,0,0]
        if intBuffer == 1:
            if vectorBuffer3[2] > 0:
                #the food is W
                hearing = [0,0,0,0,0,1]
            else :
                #the food is E
                hearing = [0,0,1,0,0,0]
        if intBuffer == 2:
            if vectorBuffer3[0] <= 0 and vectorBuffer3[1] >= 0:
                #the food is SW
                hearing = [0,0,0,0,1,0]
            else :
                #the food is NE
                hearing = [0,1,0,0,0,0]

        #-----------health sense------------------
        
        #convert the HP value to a binary vector
        binBuffer = f'{self.HP:04b}'
        healthSense = [int(j) for j in binBuffer]

        #------------seeing ----------------------
            #creates a circle around the entity that is composed of a specified amount of tiles.
            #   It then lerps between the center (the monster) and the circle tiles. When it makes
            #   contact with a 'solid' non 0 tile it ends lerping and collects the distance from
            #   the monster and the tile. They collect into a vector that is essentially the 
            #   monsters line/circle of sight


        #create vector of zeros with length of 3
        vectorBuffer1 = [0,0,0]
        #clear buffers
        vectorBuffer2 = []
        #sight range is an int to deterimine the draw limit on the monsters sight circle
        sightrange = 15
        #ray count determines how many rays are going to be casted
        raycount = 15
        #sightCircle holds all the xy locations of the tiles on a circle of sightrange radius
        #   with raycount many samples of the circle
        sightCircle = hexCircle(self.x,self.y, sightrange, raycount)
        #set the count to negative 1 (this will be used for indexes)
        count = -1
        #empty the imaginations spaces entity list and fill it with only the monsters redolent
        self.imaginationSpace.entityList = [redolent(self.x,self.y,self.appearance,rndID)]
        #create the sight vector
        sight = np.zeros(raycount)
        #iterate for each of the tiles in sightcircle
        for i in sightCircle:
            #iterate the count (1st iteration sets to 0)
            count +=1
            #set the sight circle cursors location to the cube coordinates of the current tile
            sightCircleXYZ = hex2t3(i[0], i[1])        
            #loop based on the sightrange
            for j in range(0,sightrange + 1):
                #create the lerping value
                t = (j/sightrange)
                #create the lerped x value
                vectorBuffer1[0] = lerp(bodyXYZ[0],sightCircleXYZ[0],t)
                #create the lerped y value
                vectorBuffer1[1] = lerp(bodyXYZ[1],sightCircleXYZ[1],t)
                #create the lerped z value
                vectorBuffer1[2] = lerp(bodyXYZ[2],sightCircleXYZ[2],t)
                #round the results of the lerped vector
                vectorBuffer1 = roundHex3d(vectorBuffer1[0],vectorBuffer1[1],vectorBuffer1[2])
                #convert the lerped cube coordinates to Even R coordinates
                vectorBuffer2 = hex3t2(vectorBuffer1[0],vectorBuffer1[1],vectorBuffer1[2])
                # if the lerped coordinates are valid for the gameSpace and are within the confines
                if int(vectorBuffer2[0]) >= 1 and int(vectorBuffer2[0]) <= gs.xMax - 1 and int(vectorBuffer2[1]) >= 1 and int(vectorBuffer2[1]) <= gs.yMax - 1:
                    #if the tile at the lerped coordinate is non-zero
                    if gs.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])] != 0 or j == sightrange:
                        #at the sights slot that corespond to this ray set to the distance from monster 
                        sight[count] = (hexDistance(vectorBuffer2[0],vectorBuffer2[1],self.x,self.y))
                        #draw the learned data to the imaginationSpace later planning and path finding
                        self.imaginationSpace.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])] = gs.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])]
                        #break and discontinue this ray
                        break

                    #if the tile at the lerped coordinate is a zero
                    else :
                        #iterate through the entity list to find if an entity is at the location
                        for i in gs.entityList:
                            #if there is an entity at said location
                            if int(vectorBuffer2[0]) == i.x and int(vectorBuffer2[1]) == i.y:
                                #at the sights slot that corespond to this ray set to the distance from monster     
                                sight[count] = (hexDistance(vectorBuffer2[0],vectorBuffer2[1],self.x,self.y))
                                #draw the learned data to the imaginationSpace later planning and path finding
                                self.imaginationSpace.entityList.append(redolent(i.x,i.y,i.appearance,rndID()))
                                #break and discontinue this ray
                                break
                #if the ray goes off the map
                else: 
                    #set the sight to its limit
                    sight[count] = sightrange
                    #break and discontinue this ray
                    break
        #------------sense array ----------------------
        #concatenate the collected senses into the sense array
        self.senseArray = np.concatenate((feeling,hearing), axis=None)
        self.senseArray = np.concatenate((self.senseArray,healthSense), axis=None)
        self.senseArray = np.concatenate((self.senseArray,sight), axis=None)
        #if the whole process finishes correctly return a 0
        return 0
    #----------------------------------------------------------------------------------
    #optimize uses pathfinding within the imaginationSpace to find the 'best answer' as
    #   to which direction to move and what path will eventually be taken if successful.
    #   it returns:
    #       -the optimal direction to walk at this timestep aka 'best answer'
    def optimize(self):
        #set the pathfound list to the direction and path lists returned by the pathfinder
        self.pathfound = pathFinding(self.imaginationSpace.terrainData,0,[self.x,self.y],self.foodTargetVector)
        #set the first buffer to the list of directions to walk
        vectorBuffer1 = self.pathfound[0]
        #set the second buffer to vector of zeros at size 6
        vectorBuffer2 = [0,0,0,0,0,0]
        #use error handling to guarentee that an optimal path is possible
        try:
            #if there was data returned from the path finder
            if len(vectorBuffer1) > 0:
                #set the corresponding direction to 1
                vectorBuffer2[vectorBuffer1[0]] = 1
        #if there was an error
        except TypeError as errorDetail:
            #make the sense of feeling the response (move away from walls)
            vectorBuffer2 = np.logical_not([self.senseArray[0],self.senseArray[1],self.senseArray[2],self.senseArray[3],self.senseArray[4],self.senseArray[5]])
        #set the object wide optimizeVector to the resulting vector
        self.optimizeVector = vectorBuffer2
        # return the optimal direction to walk at this timestep
        return vectorBuffer2
    #----------------------------------------------------------------------------------
    

    #----------------------------------------------------------------------------------
    #think is a function that takes the accumulated data of the gamespace that the
    #   monster has collected at the current gametick and feeds it into the NN. The
    #   output of the brain is interpreted as the direction that the entity is meant
    #   to move in. Using the optimal path data that the optimize function creates,
    #   the brain has the most correct answer fed back in as the label for 
    #   back propogation.
    def think(self):
        #tell the brain object what the senses have collected and have it feed forward
        self.brain.feedForward(self.senseArray)        
        #take the known path and feed it back into the brain and have it back propagate
        self.brain.backPropagation(self.optimizeVector)
        #if this function finishes correctly return 0
        return 0
    #----------------------------------------------------------------------------------
    
    
    #----------------------------------------------------------------------------------
    #update calls other functions in the sequential order to maintain the data flow. It
    #   also evaluates the cost for understanding the efficiency of the brain. It acts
    #   almost as the main function for the monster entity thus almost all behavior is
    #   tied directly to this function. 
    #   it takes in:
    #       -the gameSpace object
    def update(self, gs) :
        #call homeostasis
        self.homeostasis()
        #call sense creating the senseArrays latest data
        self.sense(gs)
        #use the imaginationSpace to create a 'best answer'
        self.optimize()
        #feed the data into the NN and back prop the bast ansawer
        self.think()
        #find the difference between the brains answer and the best answer, the current cost
        currentCost = pow(sum(np.subtract(self.optimizeVector ,self.brain.outputSignals)),2)
        #save the current cost to the cost list
        self.costList.append(currentCost)
        #get and save the adverage cost 
        self.cost = sum(self.costList)/self.age
        #call the move function in the direction the brain output
        self.move(np.argmax(self.brain.outputSignals), gs)
        #return 0 if the whole process worked
        return 0
    #----------------------------------------------------------------------------------
    

    #----------------------------------------------------------------------------------
    #info collects data about the monster, saves it to a file named with its id, and returns
    #   the collected data as a string
    #   returns:
    #       -info, the collected data (str)
    def info(self) :
        #save the ID first
        info = str(self.ID) +","
        #then age
        info = info + str(self.age) +","
        #then HP
        info = info + str(self.HP) + ","
        #then DNA vector
        info = info + str(self.DNA) + ","
        #then the coordinates
        info = info + str(self.x) + "," + str(self.y) + ","
        #iterate through each node of the brains input layer
        for i in range(len(self.brain.inputLayer)):
            #save the wieghts of each node
            info = info +(str(self.brain.inputLayer[i].weights)) +","
        #add comma for serperation
        info = info +  ","
        #iterate through each node of the brains hidden layer
        for i in range(len(self.brain.hiddenLayer)):
            #save the wieghts of each node
            info = info + (str(self.brain.hiddenLayer[i].weights))+ ","
        #add comma for serperation
        info = info + ","
        #iterate through each node of the brains output layer
        for i in range(len(self.brain.outputLayer)):
            #save the wieghts of each node
            info = info + (str(self.brain.outputLayer[i].weights))+ ","

        #------------save to file--------------
        #create a counter for each char to enter
        x = 0
        #create the file that will be modified and saved as the monster ID
        monsterData = open( str(self.ID) + '.txt','x')
        #loop until the info is all saved
        while x < len(info) :
            #use error handling for strange chars
            try : 
                #show that it is saving to file with a print to terminal
                print (info[x], end = '')
                #save each char to the file
                monsterData.write(info[x])
                #iterate the counter
                x += 1
            #if there is an error
            except UnicodeEncodeError as detail :
                #iterate the counter and ingore errors like a dummy
                x +=1
        #close the file
        monsterData.close
        #return the collected data
        return info
    #----------------------------------------------------------------------------------
