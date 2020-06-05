from nnode import *
from terrainGenerator import *
from hexTools import *
#create the entity classes definition
class entity :
    #all entities will have an x,y location and an ID for location in the datastructure
    def __init__(self, x, y):
        #fill the x
        self.x = x
        #fill the y
        self.y = y


class playerEntity(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y): 
        #take on the entity feature
        super().__init__(x, y)
        #set the entities type item
        self.ID = 'player'
        self.appearance = [' ꑯ', 2, 0]

class monsterEntity(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y): 
        #take on the entity feature
        super().__init__(x, y)
        #set the entities type item
        self.ID = 'monster'
        self.appearance = [' ꎒ', 1, 0]
        self.monsterAI = nnetwork(4,8,7,6,1000)

        inputlayergivenweights = [[-0.26408323,  0.00304888,  0.47521803,  0.49306502],
                                [ 0.414368,    0.52607391, -0.09492782, -0.06424611],
                                [0.15032797, 0.32169712, 0.02790114, 0.19543684],
                                [0.24323762, 0.08606071, 0.33367322, 0.18492131],
                                [ 0.40763001,  0.19445903, -0.01141685,  0.1505579 ],
                                [-0.38004605, -0.02869016,  0.35287399,  0.67925369],
                                [-0.14738504, -0.18351078,  0.34794964,  0.64173659],
                                [ 0.53052623,  0.56589614,  0.04392345, -0.26341925]]

        hiddenlayergivenweights = [[ 1.26998084, -3.90190822,  0.42000946, -1.34011473,  0.25292027,  4.04257105,  0.25821173, -0.96625124],
                                [-4.34664571, -0.04649757, -6.47495573,  5.19122825,  4.92975546, -4.97524543,  6.72584903, -1.20950291],
                                [-5.17850011,  1.97790774,  3.73422437, -8.1214061 ,  4.86837322,  0.36909592,  3.13256698, -1.39389246],
                                [-4.36966665, -0.21922247, -6.34403914,  5.2383735 ,  4.90846236, -5.01619415,  6.75705392, -1.16164529],
                                [-1.5834008 ,  3.49992949,  0.06019817, -0.95224985,  1.49001676, -2.91256058, -1.37756563,  1.76192876],
                                [ 4.91043965,  1.65301252,  5.40188301, -1.37834471, -6.55048036,  2.14183475, -7.19970837,  1.99894952],
                                [ 2.78037459, -4.50245343, -2.53547946,  4.69998874, -1.64659788,  1.67997552,  0.55384278, -1.98091874]]

        outputlayergivenweights = [[ -3.82552261,   5.26199279, -16.38682941,   4.98642068,   0.18075301,  -3.27698112,   5.50971089],
                                [  2.53391215,  -4.54083994, -19.00734088,  -5.16249219,  -3.79008576,   9.73406235,   7.82127186],
                                [ -1.23293385,  -8.6560666 ,   6.43297928,  -7.61715351,   2.36328668,  10.0006313 , -15.07785207],
                                [ 13.13252758, -10.56043687,  14.41358367,  -9.19961252,  -6.18347831, -10.27090047,   5.20913633],
                                [  6.40427945,   2.371936  ,   7.78363144,   1.68223681,  -3.10535194, -17.635366  ,   0.16914507],
                                [-13.93500052,   8.47448336,   5.02749309,   7.00788877,   1.54633638,  -7.11760818, -12.77890393]]


        for i in range(len(self.monsterAI.inputLayer)):
            self.monsterAI.inputLayer[i].weights = np.array(inputlayergivenweights[i])
        for i in range(len(self.monsterAI.hiddenLayer)):
            self.monsterAI.hiddenLayer[i].weights = np.array(hiddenlayergivenweights[i])
        for i in range(len(self.monsterAI.outputLayer)):
            self.monsterAI.outputLayer[i].weights = np.array(outputlayergivenweights[i])





def moveEntity(entityID, direction, gameSpace):
    if checkNeighbor(gameSpace.entityList[entityID].x, gameSpace.entityList[entityID].y, 0, gameSpace)[direction] == 1:
        if gameSpace.entityList[entityID].y % 2 != 0:
            if direction == 0:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y -= 1
            if direction == 1:
                gameSpace.entityList[entityID].x += 0 
                gameSpace.entityList[entityID].y -= 1
            if direction == 2:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y += 0
            if direction == 3:
                gameSpace.entityList[entityID].x += 0
                gameSpace.entityList[entityID].y += 1
            if direction == 4:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y += 1
            if direction == 5:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y += 0
        elif gameSpace.entityList[entityID].y % 2 == 0:
            if direction == 0:
                gameSpace.entityList[entityID].x += 0
                gameSpace.entityList[entityID].y -= 1
            if direction == 1:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y -= 1
            if direction == 2:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y += 0
            if direction == 3:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y += 1
            if direction == 4:
                gameSpace.entityList[entityID].x += 0
                gameSpace.entityList[entityID].y += 1
            if direction == 5:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y += 0
    #else:
        #print('the way is blocked')
    return False