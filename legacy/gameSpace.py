

def printGameSpace(gameSpace, entityList, xrange, yrange) :
    for y in range(yrange) :
        for x in range(xrange) :
            if y == 0 and x == 0:
                print ("__" * xrange)
            if x == 0:
                print ("|", end = "")
            
            
            a = False
            for z in entityList :
                if z.X == x and z.Y == y :
                    print (z.appearance, end = "")
                    a = True
                    break
            if a == False :
                print (gameSpace[x][y], end = "")
        print ("|")
        if (y == yrange-1 and x == xrange-1):
            print ("|" + "__" * xrange + "|")
def updateGameSpace(gameSpace, entityList, xrange, yrange) :
    print ("update called")
    for x in entityList :
        x.update(gameSpace, entityList)
    
   