import random
import math


def sigmoid(x) :
    return 2 / (1 + math.exp(-x)) - 1 #2/(1+e^{-x})\ -1

def Dsigmoid(x) :
    return (2 * math.exp(x)) / pow((math.exp(x) + 1), 2)                                  #sigmoid(x) * sigmoid(1 - x)        #(2*e^x)/(e^x+1)^2

class synapse :
    counter = 1

class soma :    #handles bias and 'memory' of activation, and eventually HP/ATP(stamina)?
    def __init__(self, DNA) :
        self.DNA = DNA

        self.inputMemory = [[0,0],]
        self.signalBuildupMemory = [0]
        self.signalMemory = [0]

        self.backFlowInputMemory = [[0],]
        self.backFlowSignalMemory = [0]
        self.costMemory = [0]
        self.attentionSpan = 8

class dendrite :  #input and backflow handlers
    def __init__(self, DNA) :
        self.DNA = DNA 
        self.dendriticTree = [0] 
        self.synapticWeight = [random.random() * 2 - 1]
        self.backFlowing = False

class axon :  #output and backflow activation handlers
    def __init__(self, DNA) :
        self.DNA = DNA
        self.HillockBias = random.random() * 2 - 1 # random initial bias
        self.telodendrites = [0]
        self.feedingForward = False

class neuron : #will hopefully be the building block for a neural network
    def __init__(self, DNA, x, y, ID) :
        self.DNA = DNA
        random.seed(self.DNA[0])
        self.appearance = self.DNA[3]
        self.ID = ID
        self.x = x
        self.y = y
        self.soma = soma(self.DNA)
        self.dendrite = dendrite(self.DNA)
        self.axon = axon(self.DNA)

    def feedForward(self) :

        signal = 0
        counter = 0
        
        while len(self.dendrite.dendriticTree) > len(self.dendrite.synapticWeight) :
                self.dendrite.synapticWeight.append(random.random() * 2 - 1)

        #sum of the imputs signals multiplied by the corresponding weights
        for currentBranch in self.dendrite.dendriticTree : 
            signal = signal + (currentBranch * self.dendrite.synapticWeight[counter]) 
            counter +=1
        
        # filter through the bias multiplied by the quantity of inputs
        signal = signal + self.axon.HillockBias * counter
        
        # save the memory of the signal before the sigmoid
        self.soma.signalBuildupMemory.append(signal)
        
        # sigmoid squishification resulting in a 
        signal = sigmoid(signal)
        
        #remember what signal is being sent to the axon
        self.soma.signalMemory.append(signal)
        
        #remember and then clear the input area
        shortTermMemory = []
        while counter > 0:
            shortTermMemory.insert(0, self.dendrite.dendriticTree[counter - 1])
            self.dendrite.dendriticTree[counter - 1] = 0
            counter -= 1
        self.soma.inputMemory.append(shortTermMemory)
        while counter < len(self.axon.telodendrites) :
            self.axon.telodendrites[counter] = signal
            counter += 1

        
    def backFlow(self) :

        backFlowInput = (sum(self.axon.telodendrites) / len(self.axon.telodendrites))
        self.soma.backFlowInputMemory.append(backFlowInput)
        #calculate and then store cost
        currentCost = pow(self.soma.signalMemory[-1] - backFlowInput, 2)
        self.soma.costMemory.append(currentCost)

        #calculate and then store the derivative of the sigmoid with the last buildup ran through it

        
        wieghtSensitivity = []
        inputSensitivity = []

        counter = 0
        while counter < len(self.dendrite.dendriticTree):
            # get sensitivity of weight
            wieghtSensitivity.append(self.soma.inputMemory[-1][counter] * Dsigmoid(self.soma.signalBuildupMemory[-1]) * 2 * (-self.soma.signalMemory[-1] + backFlowInput))
            # get sensitivity of inputs and thus the backflow signal to the dendrites
            inputSensitivity.append(self.dendrite.synapticWeight[counter] * Dsigmoid(self.soma.signalBuildupMemory[-1]) * 2 * (-self.soma.signalMemory[-1] + backFlowInput))
            counter += 1
        
        counter = 0
        while counter < len(self.dendrite.dendriticTree):
            # adjust weights
            self.dendrite.synapticWeight[counter] -= wieghtSensitivity[counter]
            counter += 1

        #print('weight sensitivity: ' + str(wieghtSensitivity) + ' | new weights : ' + str(self.dendrite.synapticWeight))
        #print('input sensitivity: ' + str(inputSensitivity))
        self.dendrite.dendriticTree = inputSensitivity
        self.soma.backFlowSignalMemory.append(inputSensitivity)
        
        biasSensitivity = Dsigmoid(self.soma.signalBuildupMemory[-1]) * 2 * (-self.soma.signalMemory[-1] + backFlowInput)
        self.axon.HillockBias -= biasSensitivity
        #print('bias sensitivity: ' + str(biasSensitivity) + ' | new Hillock bias: ' + str(self.axon.HillockBias))

        #remember and then clear the input area
        
        counter = len(self.axon.telodendrites)
        while counter > 0:
            self.axon.telodendrites[counter - 1] = 0
            counter -= 1

    def update(self) :


        
        #print('Neuron with ID: ' + str(self.ID) + ' has had its update function called')



        #make neuron forgetfull and if stuck randomize
        if len(self.soma.signalBuildupMemory) > self.soma.attentionSpan :
            x = int(sum(self.soma.signalBuildupMemory)) / len(self.soma.signalBuildupMemory)
            self.soma.signalBuildupMemory.clear()
            self.soma.signalBuildupMemory = [x]
        
        
        if len(self.soma.inputMemory) > self.soma.attentionSpan :
            if all(self.soma.inputMemory) and (int((self.soma.signalMemory[-1]) * 1000) == int((sum(self.soma.signalMemory) / len(self.soma.signalMemory) * 1000 ) ) ):
                for i in range(len(self.dendrite.synapticWeight)) :
                    self.dendrite.synapticWeight[i] = random.random() * 2 - 1
                self.axon.HillockBias = random.random() * 2 - 1

            self.soma.inputMemory = [self.soma.inputMemory[-1]]

        if len(self.soma.signalMemory) > self.soma.attentionSpan :
            self.soma.signalMemory = [self.soma.signalMemory[-1]]
        
        if len(self.soma.backFlowInputMemory) > self.soma.attentionSpan :
            self.soma.backFlowInputMemory = [self.soma.backFlowInputMemory[-1]]
        
        if len(self.soma.backFlowSignalMemory) > self.soma.attentionSpan :
            self.soma.backFlowSignalMemory = [self.soma.backFlowSignalMemory[-1]]
        

        if len(self.soma.costMemory) > self.soma.attentionSpan :
            x = sum(self.soma.costMemory) / len(self.soma.costMemory)
            self.soma.costMemory = [x]










        if self.axon.feedingForward != True and self.dendrite.backFlowing != True:
            if sum(self.dendrite.dendriticTree) != 0 and self.dendrite.backFlowing != True:
                self.feedForward()
                self.axon.feedingForward = True

            if sum(self.axon.telodendrites) != 0 and self.axon.feedingForward != True:
                self.backFlow()
                self.dendrite.backFlowing = True

        if (self.axon.feedingForward == True or self.dendrite.backFlowing == True) and (sum(self.axon.telodendrites) == 0 and sum(self.dendrite.dendriticTree) == 0):
            self.axon.feedingForward = False
            self.dendrite.backFlowing = False

   

    def info(self):
        outputString = 'neuron ID: ' + str(self.ID) + ' | x,y location: ' + str(self.x) + ',' + str(self.y) + ' | DNA chain ->' + str(self.DNA) + ' |\n'
        outputString += '\ndendriticTree: ' + str(self.dendrite.dendriticTree) + '\ntelodendrites: ' + str(self.axon.telodendrites) + ' | '
        outputString += '\nneuron state: '
        if self.dendrite.backFlowing:
            outputString += 'Back-flowing '
        elif self.axon.feedingForward:
            outputString += 'feeding Forward '
        else:
            outputString += 'waiting '
        nDetails = vars(self)
        dDetails = vars(self.dendrite)
        sDetails = vars(self.soma)
        aDetails = vars(self.axon)
        outputString += '\nSTATE OF THE NEURON\n' + ('\n'.join("%s: %s" % element for element in nDetails.items())) + '\n'
        outputString += '\nSTATE OF THE DENDRITE TREE\n' + ('\n'.join("%s: %s" % element for element in dDetails.items())) + '\n'
        outputString += '\nSTATE OF THE SOMA\n' + ('\n'.join("%s: %s" % element for element in sDetails.items())) + '\n'
        outputString += '\nSTATE OF THE TELODENDRITES\n' + ('\n'.join("%s: %s" % element for element in aDetails.items())) + '\n'
        
        return outputString
# stem cells to propogate and differentiate into neurons, maybe into the 4 different types for role division (maybe even glial cells?)

 # DNA TRANSCRIPTION
 # neuro transmitters glutamatergic=excite, GABAergic=inhibit, cholinergic = most signals, adrenergic = fight or flighty.
 # cholinergic for forward feed?
 # glutamatergic and GABAergic for backflow?
 # adrenergic for cost?


    