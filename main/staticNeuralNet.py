import math
import random
from eventLog import *





logger = eventLog('staticNeuralNet','0')
def sigmoid(x):
    try :
        return 2 / (1 + math.exp(-x)) - 1 #2/(1+e^{-x})\ -1
    except ArithmeticError as errorcode :
        logger.logEvent(errorcode)
        return 0 

def Dsigmoid(x) :
    try :
        return (2 * math.exp(x)) / pow((math.exp(x) + 1), 2)
    except ArithmeticError as errorcode :
        logger.logEvent(errorcode)
        return 0

class neuron : #will hopefully be the building block for a neural network
    def __init__(self, ID) :
        #random.seed(self.DNA[0])
        self.ID = ID
        self.HillockBias = random.random() * 2 - 1 # random initial bias
        self.telodendrites = [0]
        self.feedingForward = False
        self.inputMemory = [[0,0],]
        self.signalBuildupMemory = [0]
        self.signalMemory = [0]
        self.backFlowInputMemory = [[0],]
        self.backFlowSignalMemory = [0]
        self.costMemory = [0]
        self.attentionSpan = 20 
        self.dendriticTree = [0] 
        self.synapticWeight = [random.random() * 2 - 1]
        self.backFlowing = False



    def feedForward(self) :
        signal = 0
        counter = 0
        while len(self.dendriticTree) > len(self.synapticWeight) :
                self.synapticWeight.append(random.random() * 2 - 1)
        #sum of the imputs signals multiplied by the corresponding weights
        for currentBranch in self.dendriticTree : 
            signal = signal + (currentBranch * self.synapticWeight[counter]) 
            counter +=1
        # filter through the bias multiplied by the quantity of inputs
        signal = signal + self.HillockBias * counter
        # save the memory of the signal before the sigmoid
        self.signalBuildupMemory.append(signal)
        # sigmoid squishification resulting in a 
        signal = -sigmoid(signal)
        #remember what signal is being sent to the axon
        self.signalMemory.append(signal)
        #remember and then clear the input area
        shortTermMemory = []
        while counter > 0:
            shortTermMemory.insert(0, self.dendriticTree[counter - 1])
            self.dendriticTree[counter - 1] = 0
            counter -= 1
        self.inputMemory.append(shortTermMemory)
        while counter < len(self.telodendrites) :
            self.telodendrites[counter] = signal
            counter += 1

    def backFlow(self) :
        backFlowInput = (sum(self.telodendrites) / len(self.telodendrites))
        self.backFlowInputMemory.append(backFlowInput)
        #calculate and then store cost
        currentCost = pow(self.signalMemory[-1] - backFlowInput, 2)
        self.costMemory.append(currentCost)
        #calculate and then store the derivative of the sigmoid with the last buildup ran through it
        wieghtSensitivity = []
        inputSensitivity = []
        counter = 0
        while counter < len(self.dendriticTree):
            # get sensitivity of weight
            wieghtSensitivity.append(self.inputMemory[-1][counter] * Dsigmoid(self.signalBuildupMemory[-1]) * 2 * (-self.signalMemory[-1] + backFlowInput))
            # get sensitivity of inputs and thus the backflow signal to the dendrites
            inputSensitivity.append(self.synapticWeight[counter] * Dsigmoid(self.signalBuildupMemory[-1]) * 2 * (-self.signalMemory[-1] + backFlowInput))
            counter += 1
        counter = 0
        while counter < len(self.dendriticTree):
            self.synapticWeight[counter] -= wieghtSensitivity[counter]
            counter += 1
        self.dendriticTree = inputSensitivity
        self.backFlowSignalMemory.append(inputSensitivity)
        biasSensitivity = Dsigmoid(self.signalBuildupMemory[-1]) * 2 * (-self.signalMemory[-1] + backFlowInput)
        self.HillockBias -= biasSensitivity
        counter = len(self.telodendrites)
        while counter > 0:
            self.telodendrites[counter - 1] = 0
            counter -= 1

    def update(self) :
        if self.feedingForward != True and self.backFlowing != True:
            if sum(self.dendriticTree) != 0 and self.backFlowing != True:
                self.feedForward()
                self.feedingForward = True
            if sum(self.telodendrites) != 0 and self.feedingForward != True:
                self.backFlow()
                self.backFlowing = True
        if (self.feedingForward == True or self.backFlowing == True) and (sum(self.telodendrites) == 0 and sum(self.dendriticTree) == 0):
            self.feedingForward = False
            self.backFlowing = False

n1 = neuron(0)
logger.logEvent('neuron created ' + str(n1))

for i in range(100):

    n1.dendriticTree = trainingData[i]
    n1.update()
    currentGuess = n1.telodendrites[0]
    currentError = trainingData[i][-1] - n1.telodendrites[0]
    n1.telodendrites[0] = 0
    n1.update()
    n1.telodendrites[0] = currentError
    n1.update()
    n1.dendriticTree.clear()
    logger.logEvent(str(i))

logger.endLog()

