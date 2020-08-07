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
#       - the learning rate of the node 
#       - the number of inputs
#       - mode 0,1 - input array which is the staging area for inputs
#       - mode 0,1 - flowing direction
#       - mode 0,1 - lastInput array for backpropagation
#       - mode 0,1 - weights array which is size dependent on inputs
#       - mode 0,1 - bias used as a threshold/gain for results
#       - mode 0,1 - lastOutput array for backpropagation
#       - mode 0,1 - preActivationSignal for backpropagation
#       - mode 0,1 - outputSignal the staging area for the result and backprop signal
#       - mode 0,1 - backPropagationSignal used for retaining the signal during processing
#       - the feedForward function which takes the data in the inputArray and processes
#           it using weights and bias into an output signal.
#       - the backPropagation function which takes a signal put in the backPropagationSignal
#           and uses it to change the weights and biases to work towards success. This
#           also fills the inputArray for it to be fed backward to the prevoius node in
#           the network.
class nnode:
    def __init__(self, mode, learningRate, numberOfInputs):
        self.mode = mode
        self.numberOfInputs = numberOfInputs
        self.learningRate = learningRate
        # if the node is in ANN feed forward mode
        if self.mode == 0 or self.mode == 1:
            #create the input array as an empty vector
            self.inputArray = np.array([])
            #flowDirection indicates the information
            #-1 for backpropogating, 0 for nothing, 1 for forward feeding
            self.flowingDirection = 0
            #create an empty array that will record the last inputs information
            self.lastInput = np.array([])
            #create the weights as a random numbers
            self.weights = np.random.rand(self.numberOfInputs)
            #create a bias that is small
            self.bias = np.random.rand()/10
            #create an empty array to hold the last output
            self.lastOutput = np.array([])
            #the data the node holds previous to "squishification"
            self.preActivationSignal = 0
            #the int to hold the output of this node
            self.outputSignal = 0
            #the int to hold the signal/'best answer'
            self.backPropagationSignal = 0
            #if the node is a RNN
            if self.mode == 1:
                #weights for the last hidden state
                self.hiddenWeight = np.random.random()

    #------------------------------------------------------------------------------------
    #feedForward function takes the data in the inputArray and, depending on mode, processes
    #   it using weights and bias into an output signal.
    #   it returns:
    #       -the outputSignal
    def feedForward(self):
        #set the flowDirection to 1 indicating the forward feed is activated
        self.flowingDirection = 1
        #if the mode is ANN or RNN
        if self.mode == 0 or self.mode == 1:
            #calculate the preActivation signal
            self.preActivationSignal = np.dot(self.inputArray, self.weights) + self.bias
            #"squishify" the preActivationSignal and set to the outputSignal
            self.outputSignal = sigmoid(self.preActivationSignal)
            #clear the lastInput
            self.lastInput = []
            #make the last input a copy of the current input
            for i in range(len(self.inputArray)):
                self.lastInput.append(self.inputArray[i])
            #clear the input array
            self.inputArray = np.zeros(shape=(self.numberOfInputs))
            #set the lastOutput to the current output
            self.lastOutput = self.outputSignal
            #returnt the outputSignal
            return self.outputSignal
    #------------------------------------------------------------------------------------
        

    #------------------------------------------------------------------------------------
    #backPropagation takes the data in the backPropogationSignal and uses it to adjust the weights
    #   and bias with the goal of making the input result in the correct output.
    def backPropagation(self):
        #set the flowing direction to -1 as to indicate that it is backpropogating
        self.flowingDirection = -1
        #if the node is in the mode 0
        if self.mode == 0: 
            #for each of the weights in the weight array
            for w in range(len(self.weights)):
                #calculate the adjustment to the current weight a if it is positive
                if (self.weights[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput)) > 0:
                    #tell the node this weight assosiates with that it should have been active positively
                    self.inputArray[w] = 1
                #if the adjustment less than is 0
                elif(self.weights[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput)) < 0:
                    #tell the node this weight associates with that it should have been active negatively
                    self.inputArray[w] = -1
                #if the adjustment is 0
                else:
                    #tell the node associated with this weight that it should have been in active
                    self.inputArray[w] = 0
                #calculate and add the adjustments to the weight
                self.weights[w] += self.lastInput[w] * self.learningRate * Dsigmoid(self.lastOutput) * (self.backPropagationSignal - self.lastOutput) * 2
                #calculate and adjust the bias
                self.bias += sigmoid(self.preActivationSignal) * (self.backPropagationSignal - self.lastOutput)
        #clear the back Propagation Signal
        self.backPropagationSignal = 0
    #------------------------------------------------------------------------------------



