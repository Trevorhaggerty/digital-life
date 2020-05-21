from printingHandler import *


line1 = [[1,2,3,4,5,6,7,8,9,10],[1,2,3,4,5,6,7,8,9,10]]


graphRange = [40,40]
graphSpace = [ ["  " for x in range(graphRange[1]) ] for x in range(graphRange[0]) ]

printGraph(graphSpace, line1, graphRange[0], graphRange[1])
