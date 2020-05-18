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

#testing making subclasses of the entity class
class itemEntity :
    #idk looks cool though.
    def __init_subclass__(cls,entity): #<----------RAD!!
        return super().__init_subclass__()  #<----------lit breh breh