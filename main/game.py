
#import all items of the eventLog py file
from eventLog import *

#this is the definition of the game class (not the tuna class)
class game :
    #when the class is created it calls this function first
    def __init__(self):
        #create a logger and tell it what version to display
        self.logger = eventLog('digital life', '0')
        #tell the logger to be active (???this is temporary???)
        self.logger.logging = True
        #create the end condition bool and set it to false
        self.end = False
        #create the UNIVERSAL TICKER lol and set it to 0
        self.tick = 0
        #log this event (and soon every event) like a manic stenographer
        self.logger.logEvent("start program")
        #start the preGame session. this might be a menu or maybe a load screen.
        self.pregame()
        
    #pregame (or 'preh-gahm-eh') will either launch the game loop or this all just bites the dust. take your pick
    def pregame(self):
        #log the event
        self.logger.logEvent('pre-game function called')
        #this is where a menu and some declarations could go, but for now it just leaps right in
        
        #begin the game loop
        self.gameLoop()
        #return 1 because its better than 2
        return 1

    #the game falls post pregame and pre-end 
    def gameLoop(self):
        
        #log it!!!
        self.logger.logEvent('Games main loop function called')
        
        #while it isnt the end it may not always be the begining... but if it is the end, then well, end.
        while self.end != True :
            
            #log every time the loop loops and show your ticks
            self.logger.logEvent('new iteration of the game loop. Ticks:' + str(self.tick))
            
            
            #put like the game here but for now it will just end after 100 ticks
            if self.tick >= 100:
                self.end = True
            
            #iterate the ticks up. building toward more ticks than a forest that has a tick problem
            self.tick +=1


        #this is the end and we should log that
        self.logger.endLog()
        #let it be known this ended stable like a healthy relationship
        return 0
    
   
       






