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
        self.drift = False
        self.entityType = 1
        self.ID = ID
        self.appearance = "<>"
    def update(self, gameSpace, entitylist) :
        if self.drift == True:
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
        self.appearance = DNA[3]
        self.neuron = neuron(self.DNA, 0, 0 ,0)
        self.entityType = 2
        self.inputs = [[],[]]
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
        self.inputs = [0,0,0,0] #blind inputs

        #look north fill the first spot with -1 for nothing, 0 and up that say the distance north
        if self.y > 0:
            for x in range((len(gameSpace))):
                for y in range(self.y + 1) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[0] = self.y - y
        #look north fill the first spot with -1 for nothing, 0 and up that say the distance north
        if self.x < len(gameSpace)-1 :
            for x in range(self.x, (len(gameSpace))):
                for y in range(len(gameSpace[0])) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[1] = x - self.x

        if self.y < len(gameSpace[0])-1 :
            for x in range((len(gameSpace))):
                for y in range(self.y, len(gameSpace[0])) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[2] = y - self.y
        
        if self.y > 0:
            for x in range(self.x + 1):
                for y in range(len(gameSpace[0])) :
                    for z in entitylist :
                        if z.x == x and z.y == y :
                            if z.entityType == 1 :
                                self.inputs[3] = self.x - x


        return self.inputs

    def homeostasis(self):
        self.age = (datetime.datetime.now() - self.birthDateTime).total_seconds()
        
        if  self.HP < 10 and  self.HP > 0 :
            self.HP = self.HP + int((2 * self.DNA[1]) / (self.age + (self.DNA[1])))
        

    def mutate(self) :
      
        glitch = (random.randint(-1,1)) * (random.randint(-2,2))
        i = 0
        while i < len(self.DNA) :
            glitch = random.randint(-1,1)
            if i != 3: 
                self.DNA[i] += glitch
            else :
                self.DNA[i] = chr(ord(self.DNA[i]) + glitch)
            i += 1


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

        if self.neuron.dendrite.backFlowing == False and self.neuron.axon.feedingForward == False :
            self.neuron.dendrite.dendriticTree = self.perception(gameSpace, entitylist)
            self.neuron.update()
        elif self.neuron.dendrite.backFlowing == False and self.neuron.axon.feedingForward == True :
            #print(str(int(self.neuron.axon.telodendrites[0] * 4)))
            self.cellMovement(gameSpace, int(round(self.neuron.axon.telodendrites[0] * 4)))
            self.neuron.axon.telodendrites[0] = 0
            self.neuron.update()
            #back propogate correct answer
            if self.perception(gameSpace, entitylist)[0] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = 0.25 
            elif self.perception(gameSpace, entitylist)[1] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = 0.50
            elif self.perception(gameSpace, entitylist)[2] == max(self.perception(gameSpace, entitylist)) :
                self.neuron.axon.telodendrites[0] = 0.75
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
        if self.age >= self.DNA[2] and self.HP > 5 :
            self.mitosis(entitylist)
            



    def info(self) :
        info =        "look =" + self.appearance + "| sight =" + str(self.inputs) 
        info = info + "age =" + str(self.age) 
        #info = info + "cell memories ---" + (str(self.neuron.memories[0][self.neuron.circadianClock - 1])) + (str(self.neuron.memories[1][self.neuron.circadianClock - 1]))
        #info = info + "Cell DNA --------->" + str(self.DNA) + "\n"
        #info = info + "Cell location ---->" + str(self.x) + "," + str(self.y) + "\n"
        #info = info + "Cell health ------>" + str(self.HP) + "\n"
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