import numpy as np
from nnode import *
from terrainGenerator import *
from hexTools import *

#create the entity classes definition
class entity :
    #all entities will have an x,y location and an ID for location in the datastructure
    def __init__(self, x, y):
        #fill the x
        self.x = x
        #fill the y
        self.y = y
    
    def move(self,entityID, direction, gameSpace):
        if checkNeighbor(self.x, self.y, 0, gameSpace)[direction] == 0:
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
            print('the way is blocked')
        return -1

class food(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, HP):
        #take on the entity features
        super().__init__(x, y)
        #set the entities type
        self.ID = 'food'
        self.appearance = [' + ', 2, 0]
        self.HP = HP
    def update(self, gameSpace, entityList):
        return 0
 
class cell(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y, DNA):
        #take on the entity features
        super().__init__(x, y)
        #set the entities type
        self.ID = 'monster'
        self.appearance = [' ꎒ', 1, 0]
        self.DNA = DNA
        self.age = 0
        self.HP = 15
        self.brain = nnetwork(18,18,12,6,1)
        self.inputs = [ 0 for i in range(18)]
    
    def homeostasis(self):
        if self.age % 100 == 0 and self.age > 0:
            self.HP -= 1        
        self.age +=1
        return 0
    
    def sense(self, gameSpace, entitylist):
        #wall sensors -------------------------------------------------------------------------
        vectorBuffer1 = np.logical_not(checkNeighbor(self.x, self.y, 0, gameSpace)).astype(int) 
        senseArray = vectorBuffer1
        #food sensor---------------------------------------------------------------------------
            #find closest food entity
        vectorBuffer1 = []
        vectorBuffer2 = []

        for i in range(len(entitylist)):
            if entitylist[i].ID == 'food':
                vectorBuffer1.append(hexDistance(self.x,self.y, entitylist[i].x, entitylist[i].y))
                vectorBuffer2.append(i)
        print(str(vectorBuffer1) + str(vectorBuffer2))    
        intBuffer = vectorBuffer2[np.argmin(vectorBuffer1)]
        print(str(intBuffer))
        #while finished == False:
        #    min_idx = min(enumerate(vectorBuffer1)
        return 0

    def think(self):
        return 0

    def mutate(self) :
        return 0

    def apoptosis(self, entitylist):
        return 0
        
    def mitosis(self, entitylist):
        return 0

    def update(self, gameSpace, entitylist) :
        self.homeostasis()
        self.sense(gameSpace, entitylist)
        self.think()
        

        return 0
            



    def info(self) :
        #info = 'look' + str(self.appearance) + 'sight' + str(self.inputs) + 'outputs' + str(int(self.neuron.axon.telodendrites[0])) 
        #info = info + "age =" + str(self.age) 
        #info = info + 'HP' + str(self.HP) #+ "\n"
        #info = info + "cell memories ---" + (str(self.neuron.memories[0][self.neuron.circadianClock - 1])) + (str(self.neuron.memories[1][self.neuron.circadianClock - 1]))
        #info = info + "Cell DNA --------->" + str(self.DNA) + "\n"
        #info = info + "Cell location ---->" + str(self.x) + "," + str(self.y) + "\n"
        #logger.logEvent('monsters weights per layer per node',0)
        #logger.logEvent('inputlayer:',0)
        #for i in range(len(self.brain.inputLayer)):
        #    logger.logEvent(str(gameSpace.entityList[1].monsterAI.inputLayer[i].weights),0)
        #logger.logEvent('hiddenlayer:',0)
        #for i in range(len(gameSpace.entityList[1].monsterAI.hiddenLayer)):
        #    logger.logEvent(str(gameSpace.entityList[1].monsterAI.hiddenLayer[i].weights),0)
        #logger.logEvent('outputlayer:',0)
        #for i in range(len(gameSpace.entityList[1].monsterAI.outputLayer)):
        #    logger.logEvent(str(gameSpace.entityList[1].monsterAI.outputLayer[i].weights),0)
        #return info 
        return 0

