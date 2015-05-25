__author__ = 'Inspiron'
import os
import csv #TODO make sure doesn't use csv because in featureCalculationFunctions
import re
from constants import *
import numpy as np
from featureCalculationFunctions import *


def aggregate(aggregators, windowType, dataWindow, aggregatedWindows):
    aggregatedWindow = []
    if windowHasFirstRow(dataWindow):
        aggregatedWindow.append([])
    for func in aggregators:
        if windowType == 'short':
            result = func(dataWindow)
        elif windowType == 'long':
            result = func(dataWindow, aggregatedWindows)
        else: #windowType == 'entire'
            result = func(dataWindow, aggregatedWindows)
    # hand  le result if it contains field names:
    if result[0]:
        aggregatedWindow[0] += result[0]
        aggregatedWindow[1] += result[1]
    else:
        aggregatedWindow += result[1]
    return aggregatedWindow

def createTimeWindowTable(aggregatorsList, windowType, dataWindows, aggregatedWindows):
    assert len(dataWindows) == len(aggregatedWindows)
    table = []
    if windowType == 'short':
        for timeWindow in dataWindows:
            row = aggregate(aggregatorsList, windowType, timeWindow, None)
            table.append(row)
    else:
        if windowType == 'long':
            assert len(dataWindows) == len(aggregatedWindows)
        aggIter = iter(aggregatedWindows)
        for timeWindow in dataWindows:
            item = aggIter.next()
            row = aggregate(aggregatorsList, windowType, timeWindow, item)
            table.append(row)
    return table


def divideToWindows(dataMatrix, windowLength):
    # np.array(dataMatrix).shape
    firtsIteration = True
    if dataMatrix == []:
        return []
    windows =[]
    window = []
    lineCounter = 0
    for row in dataMatrix:
        lineCounter +=1
        window.append(row)
        if firtsIteration == True:
            if lineCounter == windowLength+1:
                lineCounter = 0
                windows.append(window)
                window = []
                firtsIteration = False
        else:
            if lineCounter == windowLength:
                lineCounter = 0
                windows.append(window)
                window = []
    return windows


def readFile(filePath):
    newFile = open(filePath, 'r')
    reader = csv.reader(newFile)
    allLines = [reader.next()]
    match = re.compile('(\d+\:\d+\:\d+)')
    for row in reader:
        # line = [getValue(x) for x in row]
        line = [float(value) for value in row if not match.search(value)]
        # print("line (floats): {}".format(line))
        allLines.append(line)
    return allLines

if __name__ == "__main__":
    #define the aggregators for each table
    aggregatorsListLong = []
    aggregatorsListShort = []
    aggregatorsListEntire = []

    #initialize
    dataMatrix = []
    aggregatedSubWindows = []
    aggregatedWindows = []

    counter = 0
    #create 5 sec per line table, per person
    for patient in PATIENTS:
        dataMatrix.append(readFile(DATA_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv'))
        shortAggregatedFile = open(SHORT_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        #np.array(dataMatrix).shape
        dataSubWindows = divideToWindows(dataMatrix[counter], SHORT_TIME_WINDOW)
        aggregatedSubWindows.append(createTimeWindowTable(aggregatorsListShort, 'short', dataSubWindows, None)) #TODO check if easy to return the table
        writer = csv.writer(shortAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedSubWindows[counter])
        counter += 1

    counter = 0
    #create 5 min per line table
    for patient in PATIENTS:
        longAggregatedFile = open(LONG_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        #DATA_LEN/LONG_TIME_WINDOW WINDOWS
        dataWindows = divideToWindows(dataMatrix[counter], LONG_TIME_WINDOW)
        print dataWindows
        #(DATA_LEN/SHORT_TIME_WINDOW)/(LONG_TIME_WINDOW/SHORT_TIME_WINDOW) WINDOWS = DATA_LEN/LONG_TIME
        subWindows = divideToWindows(aggregatedSubWindows[counter], LONG_TIME_WINDOW/SHORT_TIME_WINDOW)
        print subWindows
        aggregatedWindows.append(createTimeWindowTable(aggregatorsListLong, 'long', dataWindows, subWindows))
        writer = csv.writer(longAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedWindows[counter])
        counter += 1

    #create patient per line table
    #patientWindowsList = divideToPatients(dataMatrix, LongWindowsMatrix) not necesssary any more
    for patient in PATIENTS:
        entireAggregatedFile = open(ENTIRE_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        aggregatedAll = createTimeWindowTable(aggregatorsListEntire, 'entire', dataMatrix, aggregatedWindows)
        writer = csv.writer(entireAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedAll)

