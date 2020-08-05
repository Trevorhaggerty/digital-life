# ----------------------------------------------------------------------------------------
# gameSpace is an object that holds all of the data pertaining to the game play space
#   it takes in:
#       - the maximum x and y, thus the size of the gameSpace
#   it contains:
#       - the maximum x and y, thus the size of the gameSpace
#       - terrian data in the form of an array of input size
#       - a list of all the entity class objects on the gamesSpace 
#       - the current game tick / epoch
#       - the current screen count for animations and keeping track
class gameSpace:
    #required inputs
    def __init__(self, xMax, yMax):
        #variable assignment
        #the gameSpaces x y size as ints
        self.xMax = xMax
        self.yMax = yMax
        #the terrain data
        self.terrainData = [
            #made with each element holding an int of 0
            [0 for x in range(self.yMax)] for x in range(self.xMax)]
        #completely empty array for entity list
        self.entityList = []
        self.tick = 0
        self.screenCount = 0