

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