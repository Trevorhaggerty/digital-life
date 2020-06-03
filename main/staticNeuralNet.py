

#Imports---------------------------------------------------------
import numpy as np
import random
from eventLog import *
from graphHandler import *
#Global-Variable-Initialization-----------------------------------
#  name of program, version Number, priorityBias 
logger = eventLog('staticNeuralNet','0', 10) 
#logger copy paste template:    logger.logEvent('' + str(),10)


np.random.seed(seed = 1)


#training data --------------------------------------------------
    #the last element in each group is the answer
    #

trainingData = [[ 0, 0, 1, 0],
                [ 1, 1, 1, 1],
                [ 1, 0, 1, 1],
                [ 0, 1, 1, 0]]







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
        return x * (1 - x)
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

def tanh(x) :
    return np.tanh(x)

def Dtanh(x): 
        return 1.0 - tanh(x) ** 2

class node:
    def __init__(self, mode, learningRate, numberOfInputs):
        self.mode = mode
        logger.logEvent('mode:' + str(self.mode),7)
        self.inputArray = np.array([])
        self.flowingDirection = 0 # -1 for backflowing, 0 for nothing, 1 for forward flowing
        self.lastInput = np.array([])
        self.numberOfInputs = numberOfInputs
        self.learningRate = .1
 
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

        for i in range(self.numberOfInputs):
            buildup = self.inputArray[i] * self.weights[i]

        self.preActivationSignal = buildup + self.bias
        #self.outputSignal = sigmoid(self.preActivationSignal)
        self.outputSignal = sigmoid(np.dot(self.inputArray, self.weights))
        self.lastInput = self.inputArray.copy()
        self.inputArray = np.zeros(shape=(self.numberOfInputs))
        self.lastOutput = self.outputSignal
        return 1


    def backPropagation(self):
        self.flowingDirection = -1

        if self.mode == 0 : # if this is an input node the 
            for w in range(len(self.weights)) :
                self.weights[w] += self.lastInput[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput)
            #self.bias -= self.learningRate * Dsigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
        elif self.mode == 1 :
           
            logger.logEvent('input array : ' + str(self.lastInput),3)
            logger.logEvent('self.numberOfInputs - 1 : ' + str(self.numberOfInputs - 1),3)
            print(str(len(self.weights)))
            for w in range(len(self.weights)-1) :
                self.inputArray[w] += self.weights[w] * self.learningRate * Dsigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
                logger.logEvent('self.inputArray[w]' + str(self.inputArray[w]),2)
                
                self.weights[w] += self.lastInput[w] * self.learningRate * Dsigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
                logger.logEvent('self.weights[w]' + str(self.weights[w]),2)
            self.bias +=  self.learningRate * Dsigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
        
        self.backPropagationSignal = 0


def main():

    node1 = node(0, 1, 3)
    logger.logEvent('weights : ' + str(node1.weights),1)
    epochs = 10000
    while epochs > 0:
        costOverTime = []
        currentTrainingData = []
        for i in range(len(trainingData[0])):
            currentTrainingData.append(trainingData[epochs % 4][i])
        rightAnswer = currentTrainingData.pop()
        logger.logEvent('current training data' + str(currentTrainingData),3)
        node1.inputArray = np.array(currentTrainingData)
        node1.feedForward()
        logger.logEvent('weights : ' + str(node1.weights),3)
        logger.logEvent('bias : ' + str(node1.bias),3)

        logger.logEvent('         current right answer :  ' + str(rightAnswer), 3)
        logger.logEvent('         node1 output :          ' + str(node1.outputSignal), 3)
        costOverTime.append(rightAnswer - node1.outputSignal)
        node1.backPropagationSignal = rightAnswer
        node1.backPropagation()
        logger.logEvent('weights : ' + str(node1.weights),3)
        logger.logEvent('bias : ' + str(node1.bias),3)

        logger.logEvent(str(sum(costOverTime)/len(costOverTime)) + " is the cost", 3)
        logger.logEvent(str(10000 - epochs) + " epochs have passed---------------------------------------------------------", 3)
        epochs -= 1

    logger.logEvent('weights : ' + str(node1.weights),1)
    node1.inputArray = np.array([1,0,0])
    logger.logEvent('inputs [1,0,0]',1)
    node1.feedForward()
    logger.logEvent('output:' + str(node1.outputSignal),1)


main()

        