import datetime
import random
import math


class neuron:
    def __init__(self, DNA) :
        self.DNA = DNA
        random.seed(DNA[0])   #randomSeedChromisome
        self.learnedTraits = [random.random(),random.random(),random.random(),random.random(),random.random()]
        self.memories = [[],[]] # [past target locations, last decisions, keynumbers?]
        self.circadianClock = 0
        self.cost = 1
        self.moron = True
        
      
 
    
    
    def think(self, inputs) :
        # internal clock ticks
        self.circadianClock += 1
        # assess the diffrence between the result of the last action and the last decision made
        

        # current distance from target
      
        tX = 0
        tY = 0
        i = 3
        deltaDistance = 0
        while i >= 0 :
            if self.memories[0][self.circadianClock -1][i] >= 0 and i%2 == 0:
                tY = tY + self.memories[0][self.circadianClock -1][i]
            if self.memories[0][self.circadianClock -1][i] >= 0 and i%2 == 1:
                tX = tX + self.memories[0][self.circadianClock -1][i]
            i -= 1
        distanceThisFrame = math.sqrt((tX * tX) + (tY * tY))
        self.memories[0][self.circadianClock -1].append(distanceThisFrame)
        if self.circadianClock > 1 :
            deltaDistance = self.memories[0][self.circadianClock -1][4] - self.memories[0][self.circadianClock -2][4]

        self.cost = math.pow(deltaDistance - 1, 2)
        #print(str(self.cost))
        
        j = int(self.cost)
        



        #feedforward
        t = (inputs[0] * self.learnedTraits[0] + inputs[1]*self.learnedTraits[1] + inputs[2]*self.learnedTraits[2] + inputs[3]*self.learnedTraits[3]) + self.learnedTraits[4]
        #print(str(t))
        thought =  1/( 1 + (t * t)) * 4
        #print(str(thought))

  
        decision = int(thought)
        self.memories[1].append([decision,self.circadianClock])

        #============================ WHILE IN DEV MAKE OUTPUT RANDOM!!!!! ==================
        if self.moron == True :
            decision = random.randint(0,4)

        return decision
