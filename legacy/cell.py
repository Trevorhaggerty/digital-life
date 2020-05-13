import datetime
import random
import math
from neuron import *




class emptySlot:
    def __init__(self, ID):
        self.ID = ID
        self.X = -128
        self.Y = -128
        self.entityType = 0
    def update(self, a, b) :
        return 1 
    def info(self) :
        info = "slot " + str(self.ID) + " is empty"
        return info 

class foodPellet :
    def __init__(self, X, Y, Value, ID):
        self.X = X
        self.Y = Y
        self.Value = Value
        self.drift = False
        self.entityType = 1
        self.ID = ID
        self.appearance = "<>"
    def update(self, gameSpace, entitylist) :
        if self.drift == True:
            direction = random.randint(0,4)
            if direction == 1 and self.Y > 0:
                self.Y -= 1
            if direction == 2 and self.X < len(gameSpace)-1 :
                self.X += 1
            if direction == 3 and self.Y < len(gameSpace[0])-1:
                self.Y += 1
            if direction == 4 and self.X > 0:
                self.X -= 1

        return 1 
    def info(self) :
        info = ""
        return info

class cell:
    def __init__(self, DNA, X, Y, ID):
        self.DNA = DNA
        self.age = 0
        self.birthDateTime = datetime.datetime.now()
        self.HP = 10
        self.X = X
        self.Y = Y
        self.ID = ID
        self.appearance = DNA[3]
        self.neuron = neuron(self.DNA)
        self.entityType = 2
        self.inputs = [[],[]]
    
    def cellMovement(self, gameSpace, direction) :   #0 is north, 1 east, 2 south, 3 west
        if direction == 1 and self.Y > 0:
            self.Y -= 1
        if direction == 2 and self.X < len(gameSpace)-1 :
            self.X += 1
        if direction == 3 and self.Y < len(gameSpace[0])-1:
            self.Y += 1
        if direction == 4 and self.X > 0:
            self.X -= 1

    def perception(self, gameSpace, entitylist) :
        self.inputs = [-1,-1,-1,-1] #blind inputs

        #look north fill the first spot with -1 for nothing, 0 and up that say the distance north
        if self.Y > 0:
            for x in range((len(gameSpace))):
                for y in range(self.Y + 1) :
                    for z in entitylist :
                        if z.X == x and z.Y == y :
                            if z.entityType == 1 :
                                self.inputs[0] = self.Y - y
        #look north fill the first spot with -1 for nothing, 0 and up that say the distance north
        if self.X < len(gameSpace)-1 :
            for x in range(self.X, (len(gameSpace))):
                for y in range(len(gameSpace[0])) :
                    for z in entitylist :
                        if z.X == x and z.Y == y :
                            if z.entityType == 1 :
                                self.inputs[1] = x - self.X

        if self.Y < len(gameSpace[0])-1 :
            for x in range((len(gameSpace))):
                for y in range(self.Y, len(gameSpace[0])) :
                    for z in entitylist :
                        if z.X == x and z.Y == y :
                            if z.entityType == 1 :
                                self.inputs[2] = y - self.Y
        
        if self.Y > 0:
            for x in range(self.X + 1):
                for y in range(len(gameSpace[0])) :
                    for z in entitylist :
                        if z.X == x and z.Y == y :
                            if z.entityType == 1 :
                                self.inputs[3] = self.X - x


        self.neuron.memories[0].append(self.inputs)
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
        
        
        self.mutate()
        c = 0
        for x in entitylist :
            if isinstance(x, emptySlot) :
                entitylist[x.ID] = cell((self.DNA),self.X,self.Y,x.ID)
                break
            else:
                c += 1
        if c == len(entitylist) :
            entitylist.append(cell(self.DNA,self.X,self.Y,len(entitylist)))
        
        
        entitylist[self.ID] = cell(self.DNA,self.X,self.Y,self.ID)
       

        
        
        
    
    def update(self, gameSpace, entitylist) :
        self.cellMovement(gameSpace, self.neuron.think(self.perception(gameSpace,entitylist)))
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
        #info = info + "Cell location ---->" + str(self.X) + "," + str(self.Y) + "\n"
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