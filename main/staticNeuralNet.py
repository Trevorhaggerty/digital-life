

#Imports---------------------------------------------------------
import numpy as np
import random
from eventLog import *
from graphHandler import *
#Global-Variable-Initialization-----------------------------------
#  name of program, version Number, priorityBias 
logger = eventLog('staticNeuralNet','0', 1) 
#logger copy paste template:    logger.logEvent('' + str(),10)


np.random.seed(seed = 1)
learningRate = .1

#training data --------------------------------------------------
    #the last element in each group is the answer
    #
trainingData = [[0, 1],
                [1, 0],
                [2, 1],
                [3, 0],
                [4, 1],
                [5, 0],
                [6, 1],
                [7, 0],
                [8, 1],
                [9, 0],
                [10,1],
                
                
                ]








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
        logger.logEvent('mode:' + str(self.mode),7)
        self.inputArray = np.array([])
        self.flowingDirection = 0 # -1 for backflowing, 0 for nothing, 1 for forward flowing
        self.lastInput = np.array([])
        self.numberOfInputs = numberOfInputs
 
        self.weights =  np.random.rand(self.numberOfInputs)
        self.bias = random.random()

        self.lastOutput = np.array([])
        self.preActivationSignal = 0
        self.outputSignal = 0
        self.backPropagationSignal = 0

        logger.logEvent('node created with weights :' + str(self.weights),5)

    def feedForward(self):
        self.flowingDirection = 1
        #self.preActivationSignal = np.dot(self.inputArray, self.weights) + self.bias
        buildup = 0
        for i in range(self.numberOfInputs - 1):
            buildup = self.inputArray[i] * self.weights[i]
        self.preActivationSignal = buildup + self.bias
        
        
        self.outputSignal = softplus(self.preActivationSignal)
        self.lastInput = self.inputArray.copy()
        self.inputArray = np.zeros(shape=(self.numberOfInputs))
        self.lastOutput = self.outputSignal
        return 1


    def backPropagation(self):
        self.flowingDirection = -1

        if self.mode == 0 : # if this is an input node the 
            for w in range(len(self.weights)-1) :
                self.weights[w] -=  self.lastInput[w] * learningRate * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)

        elif self.mode == 1 :
            logger.logEvent('weights : ' + str(self.weights),5)
            logger.logEvent('input array : ' + str(self.lastInput),5)
            logger.logEvent('self.numberOfInputs - 1 : ' + str(self.numberOfInputs - 1),5)
            
            for w in range(len(self.weights)-1) :
                self.inputArray[w] -= self.weights[w]  * learningRate * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)
                
                logger.logEvent('self.inputArray[w]' + str(self.inputArray[w]),4)
                
                self.weights[w] -= self.lastInput[w]  * learningRate * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)
                
                logger.logEvent('self.weights[w]' + str(self.weights[w]),4)
              

        self.bias -=  learningRate * sigmoid(self.preActivationSignal) * (self.lastOutput - self.backPropagationSignal)
        self.backPropagationSignal = 0


def main():

    costList = []
    cost = 0
    node1 = node(0, 1)
    node2 = node(0, 1)
    node3 = node(1, 2)
    epoch = 0
    while epoch < 1000:
        currentTrainingDataList = []
    
        for l in range(len(trainingData[0])):
            currentTrainingDataList.append(trainingData[random.randint(0,10000) % (len(trainingData))][l])
        
        rightAnswer = currentTrainingDataList.pop()

        currentTrainingData = np.array(currentTrainingDataList)

        logger.logEvent('right answer: ' + str(rightAnswer),1)
  
       #logger.logEvent('currentTrainingData: ' + str(currentTrainingData))
 
        node1.inputArray = np.array(currentTrainingData)
        node2.inputArray = np.array(currentTrainingData)


        node1.feedForward()
        logger.logEvent('feeding forward for the first node',5)
        logger.logEvent('node1 output: ' + str(node1.outputSignal),5)
        node2.feedForward()
        logger.logEvent('feeding forward for the second node',5)
        logger.logEvent('node2 output: ' + str(node2.outputSignal),5)
        
        bufferList = [float(node1.outputSignal), float(node2.outputSignal)]
        node3.inputArray = np.array(bufferList)

        node3.feedForward()
        logger.logEvent('feeding forward for the third node',5)
        logger.logEvent('node3 output:  ' + str((node3.outputSignal)),1)

        costList.append(pow(node3.outputSignal - rightAnswer, 2))
        logger.logEvent('current cost: ' + str(pow(node3.outputSignal - rightAnswer, 2)),1)
        if len(costList) > 1 :
            cost = sum(costList)/len(costList)
            logger.logEvent('cost: ' + str(cost),2)

        node3.backPropagationSignal = rightAnswer
        node3.backPropagation()
        logger.logEvent('node backprop message to previous cell ' + str (node3.inputArray),5)
        
        node1.backPropagationSignal = node3.inputArray[0]
        node1.backPropagation()

        node2.backPropagationSignal = node3.inputArray[1]
        node2.backPropagation()

        logger.logEvent('epoch: ' + str (epoch),1)

        epoch += 1
        
    logger.logEvent('cost: ' + str(cost),1)

main    ()

        