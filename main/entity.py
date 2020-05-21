#this will contain all relevent data to create an entity and store its location

#create the entity classes definition
class entity :
    #all entities will have an x,y location and an ID for location in the datastructure
    def __init__(self, x, y, ID):
        #fill the x
        self.x = x
        #fill the y
        self.y = y
        #fill the ID
        self.ID = ID

#make a subclass of entity with the entity an Type of 'item'
class itemEntity(entity) :
    #this is the begining function for the subclass
    def __init__(self, x , y , ID , entityType ): 
        #take on the entity feature
        super().__init__(x, y, ID)
        #set the entities type item
        self.entityType = 'item'

#make the neuron
class neuron(entity) :
    #
    def __init__(self, x , y , ID , entityType ):
        #
        super().__init__(x, y, ID)
        #
        self.entityType = 'neuron'

#
