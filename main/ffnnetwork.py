from nnode import *

#----------------------------------------------------------------------------------------
#
class ffnnetwork:
    def __init__(self, numberOfInputs=2, inputLayerCount=2, hiddenLayerCount=2, outputLayerCount=1, learningRate=1):
        #
        self.learningRate = learningRate
        #
        self.numberOfInputs = numberOfInputs
        # create empty arrays for signals and the layers
        self.outputSignals = []
        self.inputLayer = []
        self.hiddenLayer = []
        self.outputLayer = []
        #
        for i in range(inputLayerCount):
            #
            self.inputLayer.append(
                #
                nnode(0, self.learningRate, self.numberOfInputs))
        #
        for i in range(hiddenLayerCount):
            #
            self.hiddenLayer.append(
                #
                nnode(0, self.learningRate, len(self.inputLayer)))
        #
        for i in range(outputLayerCount):
            #
            self.outputLayer.append(
                #
                nnode(0, self.learningRate, len(self.hiddenLayer)))
#----------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------
    #
    #
    def feedForward(self, inputData):
        #
        edgeBuffer = []
        #
        for i in range(0, len(self.inputLayer)):
            #
            self.inputLayer[i].inputArray = np.array(inputData)
            #
            self.inputLayer[i].feedForward()
            #
            edgeBuffer.append((self.inputLayer[i].outputSignal))
        #
        npEdgeBuffer = np.array(edgeBuffer)
        #
        edgeBuffer = []
        #
        for i in range(0, len(self.hiddenLayer)):
            #
            self.hiddenLayer[i].inputArray = npEdgeBuffer
            #
            self.hiddenLayer[i].feedForward()
            #
            edgeBuffer.append(self.hiddenLayer[i].outputSignal)
        #
        npEdgeBuffer = np.array(edgeBuffer)
        #
        edgeBuffer = []
        #
        for i in range(0, len(self.outputLayer)):
            #
            self.outputLayer[i].inputArray = npEdgeBuffer
            #
            self.outputLayer[i].feedForward()
            #
            edgeBuffer.append(self.outputLayer[i].outputSignal)
        #
        self.outputSignals = edgeBuffer
        #
        return 1
#----------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------
    def backPropagation(self, backPropagationSignals):
    #
        for i in range(0, len(self.outputLayer)):
            #
            self.outputLayer[i].backPropagationSignal = backPropagationSignals[i]
            #
            self.outputLayer[i].backPropagation()             
        #
        for i in range(0, len(self.hiddenLayer)):
            #
            k = 0
            #
            for j in range(0, len(self.outputLayer)):
                #
                k += self.outputLayer[j].inputArray[i]
            #
            self.hiddenLayer[i].backPropagationSignal = k/len(self.outputLayer)
            #
            self.hiddenLayer[i].backPropagation()
        #
        for i in range(0, len(self.inputLayer)):
            #
            k = 0
            #
            for j in range(0, len(self.hiddenLayer)):   
                #
                k += self.hiddenLayer[j].inputArray[i]
            #
            self.inputLayer[i].backPropagationSignal = k/len(self.outputLayer)
            #
            self.inputLayer[i].backPropagation()#