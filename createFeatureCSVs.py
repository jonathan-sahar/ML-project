__author__ = 'Inspiron'
import os
import csv
import re
from constants import *
from featureCalculationFunctions import *


def aggregate(aggregators, TimeWindow, dataWindows, aggregatedWindows):
    row = []
    for func in aggregators:
        if TimeWindow == 'short':
            result = func(dataWindows)
        elif TimeWindow == 'long':
            result = func(dataWindows, aggregatedWindows)
        else: #TimeWindow == 'entire'
            result = func(dataWindows, aggregatedWindows)
        row += result
    return row


def createTimeWindowTable(aggregatorsList, TimeWindow, dataWindows, aggregatedWindows):
    assert len(dataWindows) == len(aggregatedWindows)
    table = []
    aggIter = iter(aggregatedWindows)
    for timeWindow in dataWindows:
        row = aggregate(aggregatorsList, TimeWindow, timeWindow, aggIter.next()) #TODO eager or lazy evaluation in Python?
        table.append(row)
    return table


def divideToWindows(filePath, windowLength):
    dataFile = open(filePath)
    windows =[]
    window = []
    reader = csv.reader(dataFile)
    lineCounter = 0
    for row in reader:
        lineCounter +=1
        window.append(reader.next())
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
    return

if __name__ == "__main__":
    #define the aggregators for each table
    aggregatorsListLong = []
    aggregatorsListShort = []
    aggregatorsListEntire = []

    #initialize
    dataMatrix = []
    aggregatedSubWindows = []
    aggregatedWindows = []

    #create 5 sec per line table, per person
    for patient in PATIENTS:
        shortAggregatedFile = open(SHORT_TABLE_FILE_PATH+'_'+patient, 'w')
        dataMatrix = readFile(DATA_TABLE_FILE_PATH+'_'+patient)
        dataSubWindows = divideToWindows(dataMatrix, SHORT_TIME_WINDOW)
        aggregatedSubWindows = createTimeWindowTable(aggregatorsListShort, 'short', dataSubWindows, None) #TODO check if easy to return the table
        writer = csv.writer(shortAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedSubWindows)

    #create 5 min per line table
    for patient in PATIENTS:
        longAggregatedFile = open(LONG_TABLE_FILE_PATH+'_'+patient, 'w')
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
        entireAggregatedFile = open(ENTIRE_TABLE_FILE_PATH+'_'+patient, 'w')
        aggregatedAll = createTimeWindowTable(aggregatorsListEntire, 'entire', dataMatrix, aggregatedWindows)
        writer = csv.writer(entireAggregatedFile, lineterminator='\n')
        writer.writerows(aggregatedAll)
