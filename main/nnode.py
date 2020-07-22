#the tuna node

#Imports---------------------------------------------------------
import numpy as np
import random
from eventLog import *

#Global-Variable-Initialization-----------------------------------
#  name of program, version Number, priorityBias 
logger = eventLog('staticNeuralNet','0.2', 2, False) 
#logger copy paste template:    logger.logEvent('' + str(),10)


np.random.seed(seed = 1)



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

class nnode:
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
        #buildup = 0

        #for i in range(self.numberOfInputs):
        #    buildup = self.inputArray[i] * self.weights[i]

        #self.preActivationSignal = buildup #+ self.bias
        #self.outputSignal = sigmoid(self.preActivationSignal)

        logger.logEvent('inputArray' + str(self.inputArray),3)
        logger.logEvent('weights' + str(self.weights),3)
        print(str(self.inputArray) + '   ' + str(self.weights))
        self.outputSignal = sigmoid(np.dot(self.inputArray, self.weights) + self.bias)
        self.lastInput = []
        for i in range(len(self.inputArray)):
            self.lastInput.append(self.inputArray[i])
        self.inputArray = np.zeros(shape=(self.numberOfInputs))
        self.lastOutput = self.outputSignal
        return self.outputSignal


    def backPropagation(self):
        self.flowingDirection = -1

        if self.mode == 0 : # if this is an input node the 
            for w in range(len(self.weights)) :
                self.weights[w] += self.lastInput[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput)
            #self.bias += self.learningRate * Dsigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
        elif self.mode == 1 :
           
            for w in range(len(self.weights)) :
                
                if (reLu(self.weights[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput))) > 0:
                    self.inputArray[w] = 1
                else:
                    self.inputArray[w] = 0
                
                self.weights[w] += self.lastInput[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput)
                #logger.logEvent('self.weights[w]' + str(self.weights[w]),2)
            #self.bias +=  self.learningRate * Dsigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
        
        self.backPropagationSignal = 0




class nnetwork:
    def __init__(self, numberOfInputs=2 ,inputLayerCount = 2, hiddenLayerCount = 2, outputLayerCount = 1, learningRate = 1):
        self.learningRate = learningRate
        self.numberOfInputs = numberOfInputs


        self.outputSignals = []
        self.inputLayer = []
        self.hiddenLayer = []
        self.outputLayer = []

        for i in range(inputLayerCount):
            self.inputLayer.append(nnode(0,self.learningRate,self.numberOfInputs))
        for i in range(hiddenLayerCount):
            self.hiddenLayer.append(nnode(1,self.learningRate,len(self.inputLayer)))
        for i in range(outputLayerCount):
            self.outputLayer.append(nnode(1,self.learningRate,len(self.hiddenLayer)))
        
    def feedForward(self,inputData):
        edgeBuffer = []
        for i in range(0,len(self.inputLayer)):
            self.inputLayer[i].inputArray = np.array(inputData)
            self.inputLayer[i].feedForward()
            logger.logEvent(str(i), 3)
            logger.logEvent(str(self.inputLayer[i].outputSignal), 3)
            edgeBuffer.append((self.inputLayer[i].outputSignal))
        npEdgeBuffer = np.array(edgeBuffer)
        logger.logEvent(str(edgeBuffer),3)
        edgeBuffer = []
        for i in range(0,len(self.hiddenLayer)):
            self.hiddenLayer[i].inputArray = npEdgeBuffer
            self.hiddenLayer[i].feedForward()
            logger.logEvent(str(i), 3)
            logger.logEvent(str(self.hiddenLayer[i].outputSignal), 3)
            edgeBuffer.append(self.hiddenLayer[i].outputSignal)
        npEdgeBuffer = np.array(edgeBuffer)
        logger.logEvent(str(edgeBuffer),3)
        edgeBuffer = []
        for i in range(0,len(self.outputLayer)):
            self.outputLayer[i].inputArray = npEdgeBuffer
            self.outputLayer[i].feedForward()
            logger.logEvent(str(i), 3)
            logger.logEvent(str(self.outputLayer[i].outputSignal), 3)
            edgeBuffer.append(self.outputLayer[i].outputSignal)
        self.outputSignals = edgeBuffer
        return 1
    
    def backPropagation(self, backPropagationSignals):
        for i in range(0,len(self.outputLayer)):
            logger.logEvent('iterations in output layer progations:'+str(i),0)
            self.outputLayer[i].backPropagationSignal = backPropagationSignals[i]
            self.outputLayer[i].backPropagation()
            logger.logEvent('current nodes signal to backprop'+str(self.outputLayer[i].inputArray),0)

        for i in range(0,len(self.hiddenLayer)):
            logger.logEvent('iterations in hidden layer progations:'+str(i),0)
            k = 0
            for j in range(0,len(self.outputLayer)):
                k += self.outputLayer[j].inputArray[i]
            self.hiddenLayer[i].backPropagationSignal = k/len(self.outputLayer)
            self.hiddenLayer[i].backPropagation()
            logger.logEvent('current nodes signal to backprop'+str(self.hiddenLayer[i].inputArray),0)

        for i in range(0,len(self.inputLayer)):
            k = 0
            for j in range(0,len(self.hiddenLayer)):
                k += self.hiddenLayer[j].inputArray[i]
            self.inputLayer[i].backPropagationSignal = k/len(self.outputLayer)
            self.inputLayer[i].backPropagation()
            logger.logEvent('iterations in inputlayer progations:'+str(i),0)

            

trainingData = [[ 0, 1, 0, 0, 1],
                [ 1, 1, 1, 1, 0],
                [ 1, 0, 1, 1, 0],
                [ 0, 1, 1, 0, 1]]






#def main():
#    
#    nn = nnetwork(3,3,6,2,1)
#    epochs = 10000
#    #costOverTime = []
#    while epochs > 0:
#        rightAnswer = []
#        
#        currentTrainingData = []
#        for i in range(len(trainingData[0])):
#            currentTrainingData.append(trainingData[epochs % 4][i])
#        rightAnswer.append(currentTrainingData.pop())
#        rightAnswer.append(currentTrainingData.pop())
#        logger.logEvent('current training data' + str(currentTrainingData),1)
#        
#        nn.feedForward(np.array(currentTrainingData))
#        logger.logEvent('         current right answer :  ' + str(rightAnswer), 2)
#        logger.logEvent('                    nn output :  ' + str(nn.outputSignals), 2)
#        #costOverTime.append(rightAnswer - .outputSignal)
#        nn.backPropagation(np.array(rightAnswer))
#
#        #logger.logEvent(str(sum(costOverTime)/len(costOverTime)) + " is the cost", 3)
#        logger.logEvent(str(10000 - epochs) + " epochs have passed---------------------------------------------------------", 2)
#        epochs -= 1
#
#    #logger.logEvent('weights : ' + str(node1.weights),1)
#    #node1.inputArray = np.array([1,0,0])
#    #logger.logEvent('inputs [1,0,0]',1)
#    #node1.feedForward()
#    #logger.logEvent('output:' + str(node1.outputSignal),1)
#
#
#main()