import numpy as np
import sys
from nnode import *
from terrainGenerator import *
from hexTools import *
from mathTools import *
from printingHandler import *
from gameSpace import *
from pathfinders import *
#create the entity classes definition
class entity :
    #all entities will have an x,y location and an type for location in the datastructure
    def __init__(self, x, y, ID):
        #fill the x
        self.x = x
        #fill the y
        self.y = y

        self.ID = ID

    
    def move(self, direction, gs):
        if binNeighbor(self.x, self.y, 0, gs.terrainData)[direction] == 1:
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
            return -1            #print('the way is blocked')
        
class redolent(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, appearance, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        #set the entities type
        self.ID = ID
        self.type = 'redolent'
        self.appearance = appearance
        self.HP = 1
        self.age = 0

class food(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, HP, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        #set the entities type
        self.ID = ID
        self.type = 'food'
        self.appearance = ['(+)', 2, 0]
        self.HP = HP
        self.age = 0
    def update(self, gs, entl):
        j = 0
        for i in entl:
            if i.x == self.x and i.y == self.y and i.type == 'monster':
                self.teleport(gs)
                entl[j].HP += self.HP
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
        #set the entities type
        self.type = 'monster'
        self.DNA = DNA
        self.appearance = [(" " + chr(self.DNA[0])), self.DNA[1], 0]
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
        self.imaginationSpace = gameSpace(20, 30)
        for j in range(len(self.imaginationSpace.terrainData[0])):
            for i in range(len(self.imaginationSpace.terrainData)):
                self.imaginationSpace.terrainData[i][j] = 0
    
    def homeostasis(self, entl):
        if self.age % 25 == 0 and self.age > 0:
            self.HP -= 1
        if self.HP > 15:
            self.HP = 15
    
        self.age +=1
        return 0
    
    def sense(self, gs, entl):
        #wall sensors -------------------------------------------------------------------------
        vectorBuffer1 = np.logical_not(binNeighbor(self.x, self.y, 0, gs.terrainData)).astype(int) 
        self.feeling = vectorBuffer1
        #food sensor---------------------------------------------------------------------------
            #find closest food entity
        vectorBuffer1 = []
        vectorBuffer2 = []

        for i in range(len(entl)):
            if entl[i].type == 'food':
                vectorBuffer1.append(hexDistance(self.x,self.y, entl[i].x, entl[i].y))
                vectorBuffer2.append(i)

        intBuffer = vectorBuffer2[np.argmin(vectorBuffer1)]
        
        vectorBuffer1 = []
        vectorBuffer2 = []
        
        self.foodTargetVector = [entl[intBuffer].x,entl[intBuffer].y]

        vectorBuffer1 = hex2t3(entl[intBuffer].x,entl[intBuffer].y)
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
                vectorBuffer1[0] = int(round(lerp(bodyXYZ[0],sightCircleXYZ[0],t)))
                vectorBuffer1[1] = int(round(lerp(bodyXYZ[1],sightCircleXYZ[1],t)))
                vectorBuffer1[2] = int(round(lerp(bodyXYZ[2],sightCircleXYZ[2],t)))
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
                        for i in entl:
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
        printGameSpace(self.imaginationSpace, 0.5)
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
        try:
            if len(pathFinding) > 0:
                vectorBuffer2[vectorBuffer1[0]] = 1
        except TypeError as errorDetail:
            print(errorDetail)
            vectorBuffer2 = np.logical_not([self.senseArray[0],self.senseArray[1],self.senseArray[2],self.senseArray[3],self.senseArray[4],self.senseArray[5]])

            
        self.optimizerVector = vectorBuffer2
        return vectorBuffer2


    def mutate(self) :
        return 0

    def apoptosis(self, entl):
        #remove this entity from the entity list
        return 0
        
    def mitosis(self, entl):
        return 0

    def update(self, gs, entl) :
        self.homeostasis(entl)
        self.sense(gs, entl)
        self.optimizer()
        self.think()

        currentCost = pow(sum(np.subtract(self.optimizerVector ,self.brain.outputSignals)),2)
        self.costList.append(currentCost)
        self.cost = sum(self.costList)/self.age
        #print (str(self.cost))
        
        #if self.age <= self.maturity*self.cost:
        #    self.move(np.argmax(self.optimizerVector), gs)
        #else:
        #    self.move(np.argmax(self.brain.outputSignals), gs)
        self.move(np.argmax(self.brain.outputSignals), gs)
        
        #self.sense(gs, entl)
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

