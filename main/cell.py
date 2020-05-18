from gameSpace import colorize
import datetime
import random
import math
from neuron import *

class emptySlot:
    def __init__(self, ID):
        self.ID = ID
        self.x = -128
        self.y = -128
        self.entityType = 0 
    def update(self, a, b) :
        return 1 
    def info(self) :
        info = "slot " + str(self.ID) + " is empty"
        return info 

class foodPellet :
    def __init__(self, x, y, Value, ID):
        self.x = x
        self.y = y
        self.Value = Value
        self.drift = True
        self.entityType = 1
        self.ID = ID
        self.appearance = ["<>",2,0]
        self.updateCount = 0
    def update(self, gameSpace, entitylist) :
        self.updateCount +=1
        if self.drift == True and 1 == random.randint(1,2):
            direction = random.randint(0,4)
            if direction == 1 and self.y > 0:
                self.y -= 1
            if direction == 2 and self.x < len(gameSpace)-1 :
                self.x += 1
            if direction == 3 and self.y < len(gameSpace[0])-1:
                self.y += 1
            if direction == 4 and self.x > 0:
                self.x -= 1
        return 1 
    def info(self) :
        info = ""
        return info

class cell:
    def __init__(self, DNA, x, y, ID):
        self.DNA = DNA
        self.age = 0
        self.birthDateTime = datetime.datetime.now()
        self.HP = 10
        self.x = x
        self.y = y
        self.ID = ID
        self.appearance = [self.DNA[3],self.DNA[4],self.DNA[5]]
        self.neuron = neuron(self.DNA, 0, 0 ,0)
        self.entityType = 2
        self.inputs = [0,0,0,0]
        self.updateCount = 0
    
    def cellMovement(self, gameSpace, direction) :   #0 is north, 1 east, 2 south, 3 west
        if direction == 1 and self.y > 0:
            self.y -= 1
        if direction == 2 and self.x < len(gameSpace)-1 :
            self.x += 1
        if direction == 3 and self.y < len(gameSpace[0])-1:
            self.y += 1
        if direction == 4 and self.x > 0:
            self.x -= 1

    def perception(self, gameSpace, entitylist) :
        
        
        if self.y > 0:
            for x in range((len(gameSpace))):
                for y in range(self.y) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[0] = (self.y - y)
        else :
            self.inputs[0] = -1
        
        if self.x < len(gameSpace)-1 :
            for x in range(self.x, (len(gameSpace))):
                for y in range(len(gameSpace[0])) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[1] = (x - self.x)
        else :
            self.inputs[1] = -1

        if self.y < len(gameSpace[0])-1 :
            for x in range((len(gameSpace))):
                for y in range(self.y, len(gameSpace[0])) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[2] = (y - self.y)
        else :
            self.inputs[2] = -1
        if self.y > 0:
            for x in range(self.x):
                for y in range(len(gameSpace[0])) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[3] = (self.x - x)
        else :
            self.inputs[3] = -1
        retI = self.inputs
        return retI

    def homeostasis(self):
        self.age = self.updateCount / 25 #(datetime.datetime.now() - self.birthDateTime).total_seconds()
        
        if  self.HP < 10 and  self.HP > 0 :
            self.HP = self.HP + int((2 * self.DNA[1]) / (self.age + (self.DNA[1])))
        

    def mutate(self) :
      
        glitch = (random.randint(-1,1)) * (random.randint(-2,2))
        i = 0
        while i < len(self.DNA) :
            glitch = random.randint(-1,1)
            if i != 3 and i != 1: 
                self.DNA[i] += glitch
                
            i += 1
        glitch = random.randint(-1,1)
        self.DNA[1] = self.DNA[1] + glitch/1000
        glitch = random.randint(-1,1)
        self.DNA[3] = chr(ord(self.DNA[3]) + glitch)
        self.appearance = [self.DNA[3],self.DNA[4],self.DNA[5]]


    def apoptosis(self, entitylist):
        entitylist[self.ID] = emptySlot(self.ID)
        
    def mitosis(self, entitylist):
        c = 0
        for x in entitylist :
            if isinstance(x, emptySlot) :
                self.mutate()
                entitylist[x.ID] = cell((self.DNA),self.x + random.randint(-1,1),self.y + random.randint(-1,1),x.ID)
                break
            else:
                c += 1
        if c == len(entitylist) :
            entitylist.append(cell(self.DNA,self.x + random.randint(-1,1),self.y + random.randint(-1,1),len(entitylist)))
        
        self.mutate()
        entitylist[self.ID] = cell(self.DNA,self.x + random.randint(-1,1),self.y + random.randint(-1,1),self.ID)
       

        
        
        
    
    def update(self, gameSpace, entitylist) :
        self.updateCount += 1
        self.perception(gameSpace, entitylist)

        if self.neuron.dendrite.backFlowing == False and self.neuron.axon.feedingForward == False :
            self.neuron.dendrite.dendriticTree = self.perception(gameSpace, entitylist)
            self.neuron.update()
        elif self.neuron.dendrite.backFlowing == False and self.neuron.axon.feedingForward == True :
            #print(str(int(self.neuron.axon.telodendrites[0] * 4)))


            if self.neuron.axon.telodendrites[0] < 0 :
                self.cellMovement(gameSpace, int((self.neuron.axon.telodendrites[0]) * 2) + 3)
            elif self.neuron.axon.telodendrites[0] > 0 :
                self.cellMovement(gameSpace, int((self.neuron.axon.telodendrites[0]) * 2) + 2)
            elif self.neuron.axon.telodendrites[0] == 0 :
                if self.neuron.soma.signalMemory[-1] < 0 :
                    self.cellMovement(gameSpace, int((self.neuron.soma.signalMemory[-1]) * 2) + 3)
                elif self.neuron.soma.signalMemory[-1] > 0 :
                    self.cellMovement(gameSpace, int((self.neuron.soma.signalMemory[-1]) * 2) + 2)
            
            self.neuron.axon.telodendrites[0] = 0
            self.neuron.update()
            #back propogate correct answer
            if self.perception(gameSpace, entitylist)[0] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = -1 
            elif self.perception(gameSpace, entitylist)[1] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = -0.5
            elif self.perception(gameSpace, entitylist)[2] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = 0.5
            elif self.perception(gameSpace, entitylist)[3] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = 1
            self.neuron.update()
            self.neuron.dendrite.dendriticTree = [0]
           

        else :
            self.neuron.update()

            
 
        #print(self.neuron.info())

        self.HP -= self.age/100 * self.DNA[1]
        self.homeostasis()
        if self.HP <= 0 :
            self.apoptosis(entitylist)
        
        if self.HP > 10 :
            self.HP = 10
        if self.age >= self.DNA[2] and self.HP > 5 :
            self.mitosis(entitylist)
            



    def info(self) :
        info = colorize(self.appearance[0],self.appearance[1],self.appearance[2])
        #info = 'look' + str(self.appearance) + 'sight' + str(self.inputs) + 'outputs' + str(int(self.neuron.axon.telodendrites[0])) 
        #info = info + "age =" + str(self.age) 
        info = info + 'HP' + str(self.HP) #+ "\n"
        #info = info + "cell memories ---" + (str(self.neuron.memories[0][self.neuron.circadianClock - 1])) + (str(self.neuron.memories[1][self.neuron.circadianClock - 1]))
        #info = info + "Cell DNA --------->" + str(self.DNA) + "\n"
        #info = info + "Cell location ---->" + str(self.x) + "," + str(self.y) + "\n"
        return info 





#def 
#AT = 1
#TA = 2
#CG = 3
#GC = 4
#
#basePairs = [AT,TA,CG,GC] # Watson–Crick base pairs Adnine-Thymine, Cytosine-Guanine
#DNA = [] # list of basePairs

#TTAGGG
#AATCCC
#