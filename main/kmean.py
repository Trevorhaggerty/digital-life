
import numpy as np
import csv
from mathTools import *
from eventLog import *
logger = eventLog('kmean', '0.1', 0, False)


class kmean() :
#
    def __init__(self):
#
        np.random.seed(1)
#
        self.dataset = []
#
        self.centroids = np.array([])
#

#

#
    def loadDataSet(self, dataset, chosenColumns, weights):
#
        self.chosenColumns = chosenColumns
#
        self.weights = weights
#
        self.dataset = []
#
        for i in range(len(dataset)):
#
            self.dataset.append([])
#

#
        for i in range(len(dataset)):
#
            for j in range(len(dataset[0])):
#
                if chosenColumns[j] == 1:
#
                    self.dataset[i].append(dataset[i][j])
#
        #print(dataset)       
#

#
    def placeCentroid(self, k):
#
        self.k = k
#
        datasetDomainMin = []
#
        datasetDomainMax = []
#
        for i in range(len(self.dataset[0])):
#
            dbuffer = []
#
            for j in range(len(self.dataset)):
#
                dbuffer.append(self.dataset[j][i])
#
            datasetDomainMin.append(dbuffer[(np.argmin(np.array(dbuffer)))])
#
            datasetDomainMax.append(dbuffer[(np.argmax(np.array(dbuffer)))])
#
        #-------------------------
#
        #print(str(datasetDomainMin))
#
        #print(str(datasetDomainMax))
#
        self.centroids = np.random.rand(self.k, len(self.dataset[0]))
#
        for i in range(self.k):
#
            for j in range(len(self.dataset[0])):
#
                self.centroids[i][j] = np.random.uniform(datasetDomainMin[j],datasetDomainMax[j])
#

#

#
    def meanItteration(self, itterationCount = 1):
#
        for i in range(itterationCount):
#
            self.kGroups = []
#
            for i in range(self.k):
#
                self.kGroups.append([])       
#
            for i in range(len(self.dataset)):
#
                dbuffer = []
#
                for j in range(len(self.centroids)):
#
                    #print(str(self.dataset[i]))
#
                    dbuffer.append(wvDistance(self.centroids[j], self.dataset[i], self.weights))
#
                    #print('distance of vector to perspective centroids = ' + str(dbuffer))
#
                    #print(str(dataset[i]) + ' is closest to centroid ' + str(np.argmin(np.array(dbuffer))))
#
                self.kGroups[(np.argmin(np.array(dbuffer)))].append(self.dataset[i])
#

#
            for i in range(self.k):
#
                translationVector = np.zeros(len(self.dataset[0]))
#
                if (len(self.kGroups[i])) >= 1:
#
                    for j in range(len(self.kGroups[i])):
#
                        for l in range(len(self.kGroups[i][0])):
#
                            translationVector[l] += self.kGroups[i][j][l]
#
                    translationVector = translationVector / (len(self.kGroups[i]))
#
                    self.centroids[i] = (translationVector + self.centroids[i]) / 2
#
                else:
#
                    dbuffer = []
#
                    for j in range(len(self.kGroups)):
#
                        dbuffer.append(len(self.kGroups[j]))
#
                    #print(str(dbuffer))
#
                    #print(str(np.argmax(np.array(dbuffer))))
#
                    translationVector = self.centroids[(np.argmax(np.array(dbuffer)))]
#
                    self.centroids[i] = (translationVector + self.centroids[i]) / 2
#
            dbuffer = []
#
            for j in range(len(self.kGroups)):
#
                dbuffer.append(len(self.kGroups[j]))
#
            #print(str(dbuffer))
#

#
    def printGroups(self):
#
        for i in range(self.k):
#
        #print(str(billy.kGroups[i]))
#
            for j in range(len(self.kGroups[i])):
#
                #print(str(self.ogData[int(self.kGroups[i][j][0])][1]))# + '  ' + str(billy.kGroups[i][j]) )
#
                print (self.kGroups[i][j])
#
            print()
#

#

#
class kmeanCSV(kmean):
#
    def __init__(self):
#
        super()
#
        self.ogData = []
#

#

#

#
    def loadcsvfile(self, csvfile, rowDepth, chosenColumns, weights):
#
        self.usedColumnNames = []
#
        self.csvfile = csvfile
#
        self.dataset = []
#
        self.weights = weights
#
        with open(csvfile, newline='') as csvData:
#
            reader = csv.reader(csvData)
#
            count = 0
#
            for row in reader:
#
                self.ogData.append(row)
#
                databuffer = []
#
                if count != 0 and count < rowDepth:
#
                    for i in range(len(row)):
#
                        if chosenColumns[i] == 1:
#
                            stringBuffer = float(row[i])
#
                            databuffer.append(stringBuffer)
#
                    self.dataset.append(databuffer)
#
                elif count >= rowDepth:
#
                    break
#
                elif count == 0:
#
                    for i in range(len(row)):
#
                        if chosenColumns[i] == 1:
#
                            stringBuffer = (row[i])
#
                            databuffer.append(stringBuffer)
#
                    self.usedColumnNames.append(databuffer)
#
                count += 1
#
        #print(str(self.dataset))
#

#

#
    def printGroups(self):
#
        for i in range(self.k):
#
        #print(str(billy.kGroups[i]))
#
            for j in range(len(self.kGroups[i])):
#
                print(str(self.ogData[int(self.kGroups[i][j][0])][1]) + '  ' + str(self.kGroups[i][j]) )
#
            print()
#

#use example-------------------------------------------------------------------------

#dataset = [ [1, 1],
#            [2, 0],
#            [3, 0],
#            [4, 1],
#            [5, 1],
#]
#chosenColumns = np.ones(len(dataset[0]))
#weights = np.ones(len(dataset[0]))
#billy = kmean()
#billy.loadDataSet(dataset, chosenColumns, weights)
#billy.placeCentroid(3)
#billy.meanItteration(1)
#
#billy = kmeanCSV()
#billy.loadcsvfile('/home/cesismalon/dev/karatebrain/digital-life/main/csvfiles/HistoricalQuotes.csv', 1000,[1,0,1,1,1,1,1],[0,1,1,1,1,1])
#billy.placeCentroid(3)
#billy.meanItteration(10)
#billy.printGroups()

