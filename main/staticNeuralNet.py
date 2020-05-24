import numpy as np
import random
from eventLog import *

logger = eventLog('staticNeuralNet','0')

random.seed(0)

def sigmoid(x):
    try :
        return 1 / (1 + np.exp(-x)) 
    except ArithmeticError as errorcode :
        logger.logEvent(errorcode)
        return 0 

def Dsigmoid(x) :
    try :
        return sigmoid(x) * sigmoid(1 - x)
    except ArithmeticError as errorcode :
        logger.logEvent(errorcode)
        return 0

def reLu(x) :
    if x < 0 :
        return 0
    else:
        return x

def softplus(x) :
    try :
        return np.log(1 + np.exp(x))

    except ArithmeticError as errorcode :
        logger.logEvent(errorcode)
        return 0





class neuron:
    def __init__(self, mode, numberOfInputs):

        self.mode = mode
        self.inputArray = []
        self.flowingDirection = 0 # -1 for backflowing, 0 for nothing, 1 for forward flowing
        
        self.weights = []
        for i in range(numberOfInputs):
            self.weights.append(random.random())    
        self.bias = random.random()
        
        
        self.preActivationSignal = 0
        self.outputSignal = 0

        logger.logEvent('node created')

    def feedForward(self):
        self.flowingDirection = 1
        self.preActivationSignal = np.dot(self.inputArray,self.weights) + self.bias
        self.outputSignal = softplus(self.preActivationSignal)
        return 1

def main():
    node1 = neuron(0, 4)
    node1.inputArray = [0,1,2,3]
    node1.feedForward()
    logger.logEvent('node output: ' + str(node1.outputSignal))

main()