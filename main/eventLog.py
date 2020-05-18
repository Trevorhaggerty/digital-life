
#eventlog is the refactored and modified version of the
#java file with the same name implemented in a previous project
# written by zac and i

import datetime

# the event log class takes a log and prints it with datetime and log count
class eventLog : 

    #when the eventlog is created this is called immediately
    def __init__(self, programVersion) :

        self.programVersion = " v" + str(programVersion)
        #holds the strings for the names of columns that the log will display
        self.logColumns = "   DATE   |   TIME   |  EVENT  |  LOG ITEM"  
        #holds the number of logs done so far
        self.logCounter = 0
        #holds the date and time of each log
        self.logDate = datetime.datetime.now()
        #bool for determining if the log will be made
        self.logging = bool
        #log the new session
        self.logEvent('Begin log')
    
    #call this function when the log is closed. displays the columns names
    def endLog(self):
        if self.logging :
            self.logEvent('End log')
            print(self.logColumns)
	
    #if logging is true this formats log items, timestamps them, then prints them
    def logEvent(self, logItem) :
        #check if logging bool is true
        if self.logging :
            #if this is the first log take note and display the columns first
            if self.logCounter == 0 :
                #display splach screen
                self.splashScreen()
                #print the top column when created
                print(self.logColumns)
            #count this log
            self.logCounter +=1


#------------------Potentially its own function?------------------------#
            #make a string to hold the log count
            logCounterString = str(self.logCounter)  
    #--------------centering a string in a bounds of 7-----------
            #while the string is less than 7 characters long in total
            while len(logCounterString) < 7 :
                #if the length of the string is odd
                if len(logCounterString)%2 == 1 :
                    #add a space on the left moving the number right
                    logCounterString = " " + logCounterString 
                    #if the length of the string is even
                else :
                    #add a space on the right moving the number left
                    logCounterString = logCounterString + " "
#-----------------------------------------------------------------------#

            #update the log date to the current date and time
            self.logDate = datetime.datetime.now()
            #format the log date to fit into the confines of the columns
            self.logDate = ' ' + str(self.logDate.strftime("%d-%m-%y")) + ' | ' + str(self.logDate.strftime("%X"))
            #print the culmination of the strings with ' | ' spacers 
            print(str(self.logDate) + ' | ' +  logCounterString  + ' | ' + logItem)
            #return that the log function at least made it this far
            return 1
        #if the logging bool is false
        else:
            #return nothing because it did nothing
            return 0
	
    def splashScreen(self):
        splash = '|' + ('=' * 46 ) + '|\n'
        splash += '|digital-life' + self.programVersion + (' ' * 30) + ' |\n'	 
        splash += '|coded by                                      |\n'
        splash += '|    Trevor Haggerty  - cesismalon@gmail.com   |\n'
        splash += '|    Zachary Drummond - zdrummon@gmail.com     |\n'
        splash += '|' + ('=' * 46 ) + '|\n'
        print (splash)
        