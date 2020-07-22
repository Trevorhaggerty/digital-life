from kmean import*
from nnode import*
import numpy as np








class psuedoBrain:
    def __init__(self, inputk, outputk, instincts):
        
        self.instincts = instincts
        self.inputk = inputk
        self.outputk = outputk
        self.shortTermSensorMemory = []
        self.shortTermMemory = []
        self.longTermMemory = []

        self.pbkm = kmean()
        self.pbkm2 = kmean()
        self.age = 0
        
        self.buildpBrain()

    def buildpBrain(self):
        self.pbkm.loadDataSet(self.instincts[0],np.ones(len(self.instincts[0][0])),np.ones(len(self.instincts[0][0])))
        self.pbkm2.loadDataSet(self.instincts[1],np.ones(len(self.instincts[1][0])),np.ones(len(self.instincts[1][0])))
        self.pbkm.placeCentroid(self.inputk)
        self.pbkm2.placeCentroid(self.outputk)
        self.pbnn = nnetwork(len(self.instincts[0][0]), len(self.instincts[0][0]), int((len(self.instincts[0][0]) + len(self.instincts[1][0])) / 2), len(self.instincts[1][0]), 10)
        self.pbkm.meanItteration(5)
        self.pbkm2.meanItteration(5)
        print(str(self.pbkm.kGroups))
        print(str(self.pbkm2.kGroups))
        print(str(self.pbkm.centroids))
        print(str(self.pbkm2.centroids))

    def sense(self, data):
        self.shortTermSensorMemory.append(data)
        self.pbkm.loadDataSet(self.shortTermSensorMemory,np.ones(len(data)),np.ones(len(data)))
        self.age +=1

    def think(self):
        self.pbkm.meanItteration(1)
        
        #|-|-|-|-|-|-|-|----to be replace with batching?---|-|-|-|-|-|-|-|
        #V-V-V-V-V-V-V-V----                            ---V-V-V-V-V-V-V-V
        for i in range(len(self.pbkm.kGroups)):
            for j in range(len(self.pbkm.kGroups[i])):
                dbuffer = []
                for k in range(len(self.pbkm.kGroups[i][j])):
                    dbuffer.append((self.pbkm.kGroups[i][j][k])) 
                self.pbnn.feedForward(np.array(dbuffer))
                thought = self.pbnn.outputSignals
                self.shortTermMemory.append(thought)
                self.pbkm2.loadDataSet(self.shortTermMemory,np.ones(len(self.shortTermMemory[0])),np.ones(len(self.shortTermMemory[0])))
                self.pbkm2.meanItteration(1)
                print(str(self.pbnn.outputSignals))
                print(str(self.pbkm.kGroups))
                print(str(self.pbkm2.kGroups))


                #backprophere
                #for i in range(len(self.pbkm.kGroups)):
                #    if self.pbkm.kGroups[i].index(self.pbkm.dataset[-1]) == self.pbkm2.kGroups[i].index(self.pbkm2.dataset[-1]):
                #        print('lol')
                        
                


        self.age += 1

instincts = [[[0,0,0,0,0],[1,1,1,1,1]],[[0,0,0],[1,1,1]]]

billy = psuedoBrain(2,2,instincts)

billy.sense([1,1,0,1,1])
billy.sense([1,1,1,1,1])
billy.sense([0,0,0,0,0])
billy.think()

