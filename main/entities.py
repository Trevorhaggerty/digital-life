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
    #   it takes in:
    #       - the gameSpace
    def update(self, gs):
        j = 0
        for i in gs.entityList:
            if i.x == self.x and i.y == self.y and i.type == 'monster':
                self.teleport(gs)
                gs.entityList[j].HP += self.HP
            j += 1
        self.age += 1
        if self.age >= 100:
            self.teleport(gs)
        return 0


    def teleport(self, gs):
        looking = True
        while looking:
            x , y = np.random.randint(4,gs.xMax - 3), np.random.randint(4,gs.xMax - 3)
            if gs.terrainData[x][y] == 0:
                self.x = x
                self.y = y
                self.age = 0
                looking = False


    def info(self):
        return 0
 
class monster(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, DNA, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        self.type = 'monster'
        self.DNA = DNA
        self.appearance = ['goblin', self.DNA[1], 0 ]#[chr(self.DNA[0]-2) + chr(8272) + chr(self.DNA[0]-1), self.DNA[1], 0]
        self.age = 0
        self.HP = 15
        self.HPOld = self.HP
        self.senseArray = []
        self.hearing = []
        self.feeling = []
        self.brain = ffnnetwork(31,self.DNA[2],self.DNA[3],6,self.DNA[4])
        self.maturity = 1000
        self.inputs = [ 0 for i in range(18)]
        self.costList = [1]
        self.cost = 1
        self.foodTargetVector = []
        self.optimizerVector = []
        self.imaginationSpace = gameSpace(32, 32)
        for j in range(len(self.imaginationSpace.terrainData[0])):
            for i in range(len(self.imaginationSpace.terrainData)):
                self.imaginationSpace.terrainData[i][j] = 0
    
    def homeostasis(self, gs):
        if self.age % 25 == 0 and self.age > 0:
            self.HP -= 1
        if self.HP > 15:
            self.HP = 15
    
        self.age +=1
        return 0
    
    def sense(self, gs):
        #wall sensors -------------------------------------------------------------------------
        vectorBuffer1 = np.logical_not(binNeighbor(self.x, self.y, 0, gs.terrainData)).astype(int) 
        self.feeling = vectorBuffer1
        #food sensor---------------------------------------------------------------------------
            #find closest food entity
        vectorBuffer1 = []
        vectorBuffer2 = []

        for i in range(len(gs.entityList)):
            if gs.entityList[i].type == 'food':
                vectorBuffer1.append(hexDistance(self.x,self.y, gs.entityList[i].x, gs.entityList[i].y))
                vectorBuffer2.append(i)

        intBuffer = vectorBuffer2[np.argmin(vectorBuffer1)]
        
        vectorBuffer1 = []
        vectorBuffer2 = []
        
        self.foodTargetVector = [gs.entityList[intBuffer].x,gs.entityList[intBuffer].y]

        vectorBuffer1 = hex2t3(gs.entityList[intBuffer].x,gs.entityList[intBuffer].y)
        vectorBuffer2 = hex2t3(self.x, self.y)

        vectorBuffer3 = np.subtract(vectorBuffer1, vectorBuffer2)

        vectorBuffer1 = np.absolute(vectorBuffer3)
        intBuffer = np.argmin(vectorBuffer1)
        
        
        if intBuffer == 0:
            if vectorBuffer3[1] >= 0 and vectorBuffer3[2] <= 0:
                #print ('se')
                self.hearing = [0,0,0,1,0,0]
            else :
                #print ('nw') 
                self.hearing = [1,0,0,0,0,0]
        if intBuffer == 1:
            if vectorBuffer3[2] > 0:
                #print ('w')
                self.hearing = [0,0,0,0,0,1]
            else :
                #print ('e')
                self.hearing = [0,0,1,0,0,0]
        if intBuffer == 2:
            if vectorBuffer3[0] <= 0 and vectorBuffer3[1] >= 0:
                #print ('sw')
                self.hearing = [0,0,0,0,1,0]
            else :
                #print ('ne')
                self.hearing = [0,1,0,0,0,0]

        binBuffer = f'{self.HP:04b}'
        healthSense = [int(j) for j in binBuffer]

        vectorBuffer1 = [0,0,0]
        vectorBuffer2 = []
        vectorBuffer3 = []
        bodyXYZ = hex2t3(self.x,self.y)
        sightrange = 15
        raycount = 15
        sightCircle = hexCircle(self.x,self.y, sightrange, raycount)
        sightSamplerate = 15
        count = -1
        self.imaginationSpace.entityList = [redolent(self.x,self.y,self.appearance,rndID)]
        vectorBuffer3 = np.zeros(raycount)
        for i in sightCircle:
            count +=1
            sightCircleXYZ = hex2t3(i[0], i[1])        
            for j in range(0,sightSamplerate):
                t = (j/sightSamplerate)
                vectorBuffer1[0] = lerp(bodyXYZ[0],sightCircleXYZ[0],t)
                vectorBuffer1[1] = lerp(bodyXYZ[1],sightCircleXYZ[1],t)
                vectorBuffer1[2] = lerp(bodyXYZ[2],sightCircleXYZ[2],t)
                vectorBuffer1 = roundHex3d(vectorBuffer1[0],vectorBuffer1[1],vectorBuffer1[2])
                vectorBuffer2 = hex3t2(vectorBuffer1[0],vectorBuffer1[1],vectorBuffer1[2])
                #print (str(vectorBuffer2))
                if int(vectorBuffer2[0]) >= 1 and int(vectorBuffer2[0]) <= gs.xMax - 1 and int(vectorBuffer2[1]) >= 1 and int(vectorBuffer2[1]) <= gs.yMax - 1:
                    if gs.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])] != 0:
                        vectorBuffer3[count] = (hexDistance(vectorBuffer2[0],vectorBuffer2[1],self.x,self.y))
                        self.imaginationSpace.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])] = gs.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])]
                        break
                    elif j == sightrange:
                        vectorBuffer3[count] = (hexDistance(vectorBuffer2[0],vectorBuffer2[1],self.x,self.y))
                        self.imaginationSpace.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])] = gs.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])]
                        break
                    else :
                        for i in gs.entityList:
                            if int(vectorBuffer2[0]) == i.x and int(vectorBuffer2[1]) == i.y:
                                vectorBuffer3[count] = (hexDistance(vectorBuffer2[0],vectorBuffer2[1],self.x,self.y))
                                self.imaginationSpace.entityList.append(redolent(i.x,i.y,i.appearance,rndID()))
                                break
                        #self.imaginationSpace.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])] = gs.terrainData[int(vectorBuffer2[0])][int(vectorBuffer2[1])]
                else: 
                    vectorBuffer3[count] = 15
                    break
            
        #print(str(vectorBuffer3))
        self.senseArray = np.concatenate((self.feeling,self.hearing), axis=None)
        self.senseArray = np.concatenate((self.senseArray,healthSense), axis=None)
        self.senseArray = np.concatenate((self.senseArray,vectorBuffer3), axis=None)

        vectorBuffer1 = [self.x, self.y]
        pathfound = pathFinding(self.imaginationSpace.terrainData,0,vectorBuffer1,self.foodTargetVector,1)
        
        #print(str(pathfound))
        for i in pathfound:
            self.imaginationSpace.terrainData[i[0]][i[1]] = -2
        #for i in range(9):
        #    printGameSpace(self.imaginationSpace, [self.x,self.y], [20, 20], 0.05)

        #print(str(self.senseArray))
        #while finished == False:
        #    min_typex = min(enumerate(vectorBuffer1)
        return 0

    def think(self):
        self.brain.feedForward(self.senseArray)
        
        self.brain.backPropagation(self.optimizerVector)

        #print(str(self.brain.outputSignals) + str(self.HP))
        #print(str(vectorBuffer2))
        return 0

    def optimizer(self):
        for y in range(self.imaginationSpace.yMax):
            for x in range(self.imaginationSpace.xMax):
                if self.imaginationSpace.terrainData[x][y] == -2:
                    self.imaginationSpace.terrainData[x][y] = 0
        vectorBuffer1 = pathFinding(self.imaginationSpace.terrainData,0,[self.x,self.y],self.foodTargetVector)
        vectorBuffer2 = [0,0,0,0,0,0]
        try:
            if len(vectorBuffer1) > 0:
                vectorBuffer2[vectorBuffer1[0]] = 1
                #print(str(vectorBuffer2))
        except TypeError as errorDetail:
           # print(errorDetail)
            vectorBuffer2 = np.logical_not([self.senseArray[0],self.senseArray[1],self.senseArray[2],self.senseArray[3],self.senseArray[4],self.senseArray[5]])

            
        self.optimizerVector = vectorBuffer2
        return vectorBuffer2


    def mutate(self) :
        return 0

    def apoptosis(self, gs):
        #remove this entity from the entity list
        return 0
        
    def mitosis(self, gs):
        return 0

    def update(self, gs) :
        self.homeostasis(gs)
        self.sense(gs)
        self.optimizer()
        self.think()

        currentCost = pow(sum(np.subtract(self.optimizerVector ,self.brain.outputSignals)),2)
        self.costList.append(currentCost)
        self.cost = sum(self.costList)/self.age
        self.move(np.argmax(self.brain.outputSignals), gs)
        
        return 0
            



    def info(self) :
        print('------------------------------------------------------------------------------------------------')
        #info = 'look' + str(self.appearance) + 'sight' + str(self.inputs) + 'outputs' + str(int(self.neuron.axon.telodendrites[0])) 
        info = str(self.ID) +","
        info = info + str(self.age) +","
        info = info + str(self.HP) + ","
        info = info + str(self.DNA) + ","
        info = info + str(self.x) + "," + str(self.y) + ","
           
        for i in range(len(self.brain.inputLayer)):
            info = info +(str(self.brain.inputLayer[i].weights)) +","

        info = info +  ","
        for i in range(len(self.brain.hiddenLayer)):
            info = info + (str(self.brain.hiddenLayer[i].weights))+ ","
        info = info + ","
        for i in range(len(self.brain.outputLayer)):
            info = info + (str(self.brain.outputLayer[i].weights))+ ","
        #return info 
        x = 0
        chrValues = open( str(self.ID) + '.txt','x')
        while x < len(info) :
            try :
                print (info[x], end = '')
                chrValues.write(info[x])
                x += 1
            except UnicodeEncodeError as detail :
                x +=1

        chrValues.close
        return info

