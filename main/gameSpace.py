from mathTools import rndID

# ----------------------------------------------------------------------------------------
# Hextile is an object that holds the properties of the tiles that compose the gameSpace
#   they retain information about the substance and reactivity of the tile.
#   it contains:
#       - an ID for keeping track of individual tiles (uuid4)
#       - the tiles type (int)
class tile:
    #it requires no inputs to spawn but can be heavily modified later on
    def __init__(self):
        self.ID = rndID
        self.tileType = 0

# ----------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------
# gameSpace is an object that holds all of the data pertaining to the gamePlay space
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
        #the time keeping value
        self.tick = 0
        #the times the screen has been printed
        self.screenCount = 0
# ----------------------------------------------------------------------------------------