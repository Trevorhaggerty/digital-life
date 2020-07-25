import numpy as np
from nnode import *
from terrainGenerator import *
from hexTools import *

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
        if checkNeighbor(self.x, self.y, 0, gs)[direction] == 1:
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
        

class food(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, HP, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        #set the entities type
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
            x , y = np.random.randint(3,gs.xMax - 3), np.random.randint(3,gs.xMax - 3)
            if gs.terrainData[x][y] == 0:
                self.x = x
                self.y = y
                self.age = 0
                looking = False
    def info(self):
        return 0
 
class cell(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, DNA, ID):
        #take on the entity features
        super().__init__(x, y, ID)
        #set the entities type
        self.type = 'monster'
        self.appearance = [' ꎒ', 1, 0]
        self.DNA = DNA
        self.age = 0
        self.HP = 15
        self.HPOld = self.HP
        self.senseArray = []
        self.hearing = []
        self.feeling = []
        self.brain = nnetwork(16,16,12,6,1)
        self.inputs = [ 0 for i in range(18)]
    
    def homeostasis(self, entl):
        if self.age % 25 == 0 and self.age > 0:
            self.HP -= 1
        if self.HP > 15:
            self.HP = 15
    
        self.age +=1
        return 0
    
    def sense(self, gs, entl):
        #wall sensors -------------------------------------------------------------------------
        vectorBuffer1 = np.logical_not(checkNeighbor(self.x, self.y, 0, gs)).astype(int) 
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

        vectorBuffer1 = []
        binBuffer = f'{self.HP:04b}'
        vectorBuffer1 = [int(j) for j in binBuffer]


        self.senseArray = np.concatenate((self.feeling,self.hearing), axis=None)
        self.senseArray = np.concatenate((self.senseArray,vectorBuffer1), axis=None)
        #print(str(self.senseArray))

        #while finished == False:
        #    min_typex = min(enumerate(vectorBuffer1)
        return 0

    def think(self):
        self.brain.feedForward(self.senseArray)
        vectorBuffer1 = np.subtract(np.multiply(self.hearing,np.array([1.5 for i in range(6)])), self.feeling)

        vectorBuffer1 = np.add(vectorBuffer1, np.logical_not(self.feeling.astype(int)))
        for i in range(len(vectorBuffer1)):
            if vectorBuffer1[i] < 0:
                vectorBuffer1[i] = 0
        vectorBuffer2 = [0,0,0,0,0,0]
        vectorBuffer2[np.argmax(vectorBuffer1)] = 1

        self.brain.backPropagation(vectorBuffer1)

        #print(str(self.brain.outputSignals) + str(self.HP))
        #print(str(vectorBuffer2))
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
        if self.age%3 == 0:
            self.move(np.argmax(self.think()), gs)
        else:
            self.think()
            self.move(np.argmax(self.brain.outputSignals), gs)
        return 0
            



    def info(self) :
        print('------------------------------------------------------------------------------------------------')
        #info = 'look' + str(self.appearance) + 'sight' + str(self.inputs) + 'outputs' + str(int(self.neuron.axon.telodendrites[0])) 
        #info = info + "age =" + str(self.age) 
        print( 'HP : ' + str(self.HP)) #+ "\n"
        #info = info + "cell memories ---" + (str(self.neuron.memories[0][self.neuron.circadianClock - 1])) + (str(self.neuron.memories[1][self.neuron.circadianClock - 1]))
        #info = info + "Cell DNA --------->" + str(self.DNA) + "\n"
        #info = info + "Cell location ---->" + str(self.x) + "," + str(self.y) + "\n"
        print('monsters weights per layer per node')
        print('inputlayer:')
    
        for i in range(len(self.brain.inputLayer)):
            print(str(self.brain.inputLayer[i].weights))

        print('hiddenlayer:')
        for i in range(len(self.brain.hiddenLayer)):
            print(str(self.brain.hiddenLayer[i].weights))
        print('outputlayer:')
        for i in range(len(self.brain.outputLayer)):
            print(str(self.brain.outputLayer[i].weights))
        #return info 
        return 0

