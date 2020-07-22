
import numpy as np
import csv
from mathTools import *

class kmean() :
    def __init__(self, k, steps, csvfile, rowDepth, chosenColumns, weights):
        np.random.seed(1)
        self.k = k
        self.dataset = []
        self.weights = weights
        self.centroids = np.array([])
        self.kGroups = []
        self.ogData = []
        self.usedColumnNames = []
        #print(str(self.dataset))

        with open(csvfile, newline='') as csvData:
            reader = csv.reader(csvData)
            count = 0
            for row in reader:
                self.ogData.append(row)
                databuffer = []
                if count != 0 and count < rowDepth:
                    for i in range(len(row)):
                        if chosenColumns[i] == 1:
                            stringBuffer = float(row[i])
                            databuffer.append(stringBuffer)
                    self.dataset.append(databuffer)
                elif count >= rowDepth:
                    break
                elif count == 0:
                    for i in range(len(row)):
                        if chosenColumns[i] == 1:
                            stringBuffer = (row[i])
                            databuffer.append(stringBuffer)
                    self.usedColumnNames.append(databuffer)
                count += 1
        #print(str(self.dataset))

        for i in range(k):
            self.kGroups.append([])
        self.placeCentroid()
        for i in range(steps):
            self.meanItteration()



    def placeCentroid(self):
        datasetDomainMin = []
        datasetDomainMax = []
        for i in range(len(self.dataset[1])):
            dbuffer = []
            for j in range(len(self.dataset)):
                dbuffer.append(self.dataset[j][i])
            datasetDomainMin.append(dbuffer[(np.argmin(np.array(dbuffer)))])
            datasetDomainMax.append(dbuffer[(np.argmax(np.array(dbuffer)))])
        #-------------------------
        #print(str(datasetDomainMin))
        #print(str(datasetDomainMax))
        self.centroids = np.random.rand(self.k, len(self.dataset[1]))
        for i in range(self.k):
            for j in range(len(self.dataset[1])):
                self.centroids[i][j] = np.random.uniform(datasetDomainMin[j],datasetDomainMax[j])

           
    def meanItteration(self):
        self.kGroups = []
        for i in range(self.k):
            self.kGroups.append([])       
        for i in range(len(self.dataset)):
            dbuffer = []
            for j in range(len(self.centroids)):
                dbuffer.append(wmdDistance(self.centroids[j], self.dataset[i], self.weights))
            #print('distance of vector to perspective centroids = ' + str(dbuffer))
            #print(str(dataset[i]) + ' is closest to centroid ' + str(np.argmin(np.array(dbuffer))))
            self.kGroups[(np.argmin(np.array(dbuffer)))].append(self.dataset[i])
        
        for i in range(self.k):
            translationVector = np.zeros(len(self.dataset[0]))
            if (len(self.kGroups[i])) >= 1:
                for j in range(len(self.kGroups[i])):
                    for l in range(len(self.kGroups[i][0])):
                        translationVector[l] += self.kGroups[i][j][l]
                translationVector = translationVector / (len(self.kGroups[i]))
                self.centroids[i] = (translationVector + self.centroids[i]) / 2
            else:
                dbuffer = []
                for j in range(len(self.kGroups)):
                    dbuffer.append(len(self.kGroups[j]))
                #print(str(dbuffer))
                #print(str(np.argmax(np.array(dbuffer))))
                translationVector = self.centroids[(np.argmax(np.array(dbuffer)))]
                self.centroids[i] = (translationVector + self.centroids[i]) / 2
        dbuffer = []
        for j in range(len(self.kGroups)):
            dbuffer.append(len(self.kGroups[j]))
        print(str(dbuffer))

    def printGroups(self):
        for i in range(self.k):
        #print(str(billy.kGroups[i]))
            for j in range(len(self.kGroups[i])):
                print(str(self.ogData[int(self.kGroups[i][j][0])][1]))# + '  ' + str(billy.kGroups[i][j]) )
            print()







#billy = kmean(10, 50, '/home/cesismalon/dev/karatebrain/digital-life/main/csvfiles/vgsales.csv', 500,[1,0,0,1,0,0,1,1,1,1,1],[0,0,1,1,1,1,1])
billy = kmean(7, 100, '/home/cesismalon/dev/karatebrain/digital-life/main/csvfiles/zoo.csv', 102,[1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,1,1,1,1.1,1,1,1,1,1,1.1,1,1,1,1,1,1,12],)
billy.printGroups()

