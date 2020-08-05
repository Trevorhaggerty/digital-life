# the tuna node

# Imports---------------------------------------------------------
import numpy as np
import random
from eventLog import *
from mathTools import *

# Global-Variable-Initialization-----------------------------------
#  name of program, version Number, priorityBias
logger = eventLog('staticNeuralNet', '0.3', 10, False)
# logger copy paste template:    logger.logEvent('' + str(),10)

logger.priorityBias = 1
np.random.seed(seed=1)

# ----------------------------------------------------------------------------------------
# nnode is a node for neural networks. 
#   it takes in:
#       - the mode of the neuron 0 = feed forward, 1 = rnn, 2 = lstm, 3 = kmean
#       - the learning rate of the node
#       - the number of inputs for the sizing weight vector
#   it contains:
#       - the mode of the neuron
#       -
#       -
#       - mode 0 - 
#       - mode 0 -
#       - mode 0 -
#       - mode 0 -
#       - mode 0 -
#       - mode 0 -
#       - mode 0 -
#       - mode 0 -
#       - mode 0 -
class nnode:
    def __init__(self, mode, learningRate, numberOfInputs):
        self.mode = mode
        self.numberOfInputs = numberOfInputs
        self.learningRate = learningRate

        if self.mode == 0:
            logger.logEvent('mode:' + str(self.mode), 7)
            self.inputArray = np.array([])
            self.flowingDirection = 0  # -1 for backflowing, 0 for nothing, 1 for forward flowing
            self.lastInput = np.array([])

            self.weights = np.subtract(
                np.ones(self.numberOfInputs), np.random.rand(self.numberOfInputs))
            self.bias = np.random.random()/10

            self.lastOutput = np.array([])
            self.preActivationSignal = 0
            self.outputSignal = 0
            self.backPropagationSignal = 0

        logger.logEvent('node created with weights :' + str(self.weights), 5)

    def feedForward(self):
        self.flowingDirection = 1
        if self.mode == (0):
            self.preActivationSignal = np.dot(
                self.inputArray, self.weights) + self.bias
            logger.logEvent('inputArray' + str(self.inputArray), 3)
            logger.logEvent('weights' + str(self.weights), 3)
            self.outputSignal = sigmoid(
                np.dot(self.inputArray, self.weights) + self.bias)
            self.lastInput = []
            for i in range(len(self.inputArray)):
                self.lastInput.append(self.inputArray[i])
            self.inputArray = np.zeros(shape=(self.numberOfInputs))
            self.lastOutput = self.outputSignal
            return self.outputSignal
    def backPropagation(self):
        self.flowingDirection = -1
        if self.mode == 0: 
            for w in range(len(self.weights)):
                self.weights[w] += self.lastInput[w] * self.learningRate * Dsigmoid(
                    self.lastOutput) * (self.backPropagationSignal - self.lastOutput) * 2
                if (self.weights[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput)) > 0:
                    self.inputArray[w] = 1
                else:
                    self.inputArray[w] = 0
                logger.logEvent('self.weights[w]' + str(self.weights[w]),2)
            self.bias += sigmoid(self.preActivationSignal) * \
                (self.backPropagationSignal - self.lastOutput)
        self.backPropagationSignal = 0



