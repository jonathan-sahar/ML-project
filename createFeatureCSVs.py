__author__ = 'Inspiron'
import os
import csv #TODO make sure doesn't use csv because in featureCalculationFunctions
import re
from constants import *
import numpy as np
#from featureCalculationFunctions import *


def aggregate(aggregators, windowType, dataWindow, aggregatedWindows):
    #print dataWindow
    row = []
    for func in aggregators:
        if windowType == 'short':
            result = func(dataWindow)
            #print result
        elif windowType == 'long':
            result = func(dataWindow, aggregatedWindows)
        else: #windowType == 'entire'
            result = func(dataWindow, aggregatedWindows)
        #print result
        row += result
        #x = row+result
        #print x

    return row


def createTimeWindowTable(aggregatorsList, windowType, dataWindows, aggregatedWindows):
    print dataWindows
    table = []
    if windowType == 'short':
        for timeWindow in dataWindows:
            row = aggregate(aggregatorsList, windowType, timeWindow, None)
            table.append(row)
    else:
        assert len(dataWindows) == len(aggregatedWindows)
        aggIter = iter(aggregatedWindows)
        for timeWindow in dataWindows:
            item = aggIter.next()
            row = aggregate(aggregatorsList, windowType, timeWindow, item)
            table.append(row)
    return table


def divideToWindows(dataMatrix, windowLength):
    # np.array(dataMatrix).shape
    if dataMatrix == []:
        return []
    windows =[]
    window = []
    lineCounter = 0
    for row in dataMatrix:
        lineCounter +=1
        window.append(row)
        if lineCounter == windowLength:
            lineCounter = 0
            windows.append(window)
            window = []
    return windows


def readFile(filePath):
    allLines = []
    newFile = open(filePath, 'r')
    reader = csv.reader(newFile)
    for row in reader:
        allLines.append(row)
    return allLines

def foo(valueList):
    return [3]

if __name__ == "__main__":
    #define the aggregators for each table
    aggregatorsListLong = [foo]
    aggregatorsListShort = [foo]
    aggregatorsListEntire = [foo]

    #initialize
    dataMatrix = []
    aggregatedSubWindows = []
    aggregatedWindows = []

    #create 5 sec per line table, per person
    for patient in PATIENTS:
        dataMatrix = readFile(DATA_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv')
        shortAggregatedFile = open(SHORT_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        #np.array(dataMatrix).shape
        dataSubWindows = divideToWindows(dataMatrix, SHORT_TIME_WINDOW)
        aggregatedSubWindows = createTimeWindowTable(aggregatorsListShort, 'short', dataSubWindows, None) #TODO check if easy to return the table
        writer = csv.writer(shortAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedSubWindows)

    #create 5 min per line table
    for patient in PATIENTS:
        longAggregatedFile = open(LONG_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        #DATA_LEN/LONG_TIME_WINDOW WINDOWS
        dataWindows = divideToWindows(dataMatrix, LONG_TIME_WINDOW)
        #(DATA_LEN/SHORT_TIME_WINDOW)/(LONG_TIME_WINDOW/SHORT_TIME_WINDOW) WINDOWS = DATA_LEN/LONG_TIME
        subWindows = divideToWindows(aggregatedSubWindows, LONG_TIME_WINDOW/SHORT_TIME_WINDOW)
        aggregatedWindows = createTimeWindowTable(aggregatorsListLong, 'long', dataWindows, subWindows)
        writer = csv.writer(longAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedWindows)

    #create patient per line table
    #patientWindowsList = divideToPatients(dataMatrix, LongWindowsMatrix) not necesssary any more
    for patient in PATIENTS:
        entireAggregatedFile = open(ENTIRE_TABLE_FILE_PATH[:-4]+'_'+patient+'.csv', 'w')
        aggregatedAll = createTimeWindowTable(aggregatorsListEntire, 'entire', dataMatrix, aggregatedWindows)
        writer = csv.writer(entireAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedAll)


'''
import csv
path = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\HumDynLog_APPLE_LGE_LGE_A0000028AF9C96_20111220_115329_20111220_120000\hdl_accel_APPLE_20111220_115330.csv'
dataFile = open(path, 'r')
reader = csv.reader(dataFile)
for row in reader:
    print row
print window
'''
