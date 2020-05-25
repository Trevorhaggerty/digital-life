#Imports---------------------------------------------------------

import numpy as np
import random
from eventLog import *

#Global-Variable-Initialization-----------------------------------

logger = eventLog('staticNeuralNet','0')
random.seed(5)

#Activation Functions --------------------------------------------
    #Sigmoid and its derivative-----------------------------------
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
    #reLu and its derivative--------------------------------------
def reLu(x) :
    if x < 0 :
        return 0
    else:
        return x

def DreLu(x) :
    if x < 0 :
        return 0
    else:
        return 1
    #softplus (the derivative of the softplus is the sigmoid)-----
def softplus(x) :
    try :
        return np.log(1 + np.exp(x)) - 1
    except ArithmeticError as errorcode :
        logger.logEvent(errorcode)
        return 0


class node:
    def __init__(self, mode, numberOfInputs):

        self.mode = mode
        self.inputArray = []
        self.flowingDirection = 0 # -1 for backflowing, 0 for nothing, 1 for forward flowing
        self.lastInput = []
        
        self.weights = []
        for i in range(numberOfInputs):
            self.weights.append(random.random())    
        self.bias = random.random()

        self.lastOutput = 0
        self.preActivationSignal = 0
        self.outputSignal = 0
        self.backPropagationSignal = 0

        logger.logEvent('node created')

    def feedForward(self):
        self.flowingDirection = 1
        self.preActivationSignal = np.dot(self.inputArray,self.weights) + self.bias
        self.outputSignal = softplus(self.preActivationSignal)
        self.lastInput = self.inputArray
        for i in range(len(self.inputArray)):
            self.inputArray[i] = 0
        self.lastOutput = self.outputSignal
        return 1


    def backPropagation(self):
        self.flowingDirection = -1

        if self.mode == 0 : # if this is an input node the 
            for w in range(len(self.weights)) :
                self.weights[w] -= 2 * self.lastInput[w] * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)

        elif self.mode == 1 :
            for w in range(len(self.weights)) :
                self.inputArray[w] = 2 * self.lastInput[w] * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)
                self.weights[w] += 2 * self.lastInput[w] * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)

        self.bias -= 2 * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)
        self.backPropagationSignal = 0


def main():

    rightAnswer = random.randint(-1,3)

    node1 = node(0, 4)
    sessions = 0
    while sessions < 50:
        node1.inputArray = [1,0.1,0.5,0.3]
        node1.feedForward()
        logger.logEvent('node output: ' + str(node1.outputSignal))
        cost = pow(node1.outputSignal - rightAnswer, 2)
        node1.backPropagationSignal = rightAnswer
        node1.backPropagation()
        logger.logEvent('node backprop message to previous cell ' + str (node1.inputArray))
        logger.logEvent('sessions: ' + str (sessions))
        sessions += 1
    
main    ()