

class gameSpace:
    def __init__(self, xMax, yMax):
        self.xMax = xMax
        self.yMax = yMax
        self.terrainData = [[ 0 for x in range(self.yMax) ] for x in range(self.xMax) ]
        self.entityList = []
