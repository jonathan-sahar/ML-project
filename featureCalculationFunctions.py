__author__ = 'Jonathan'
import numpy as np
import scipy.stats as stats
import csv

LONG_TIME_WINDOW = 300
SHORT_TIME_WINDOW = 5

def stats1(timeWindow, timeWindowLength, filePath):
    func_pointers = [(stats.tmax, 'max'), (stats.tmin,'min' ), (stats.trim_mean,'mean'), (stats.m)] #TODO add more functions and tuple with feature name

    data = []
    reader = csv.reader(filePath)
    for row in reader:
        data.append(row)
    data = np.array(data)
    for column in data.T:
        values = [func(column) for func in func_pointers]
    return values

def statsForLongTimeWindow():

def statsForLongTimeWindow():

def lowFreqsCounter(window, shortTimeWindowPath):
    #if isLongTimeWindow == 0:
     #   return [] #TODO assert this
    numberOfrows = LONG_TIME_WINDOW/SHORT_TIME_WINDOW
    data = []
    shortTimeWindowFile = open(shortTimeWindowPath)
    reader = csv.reader(shortTimeWindowFile)
    row = reader.next()
    columbs = row.split(',')
    index = columbs.index('lowFreq') #TODO this is the name?
    lineCounter = 0
    thresholdCounter = 0
    for row in reader:
        columbs = row.split(',')
        if columbs[index] == 1:
            thresholdCounter+=1
        if lineCounter == numberOfrows - 1:
            data.append(thresholdCounter)
            thresholdCounter = 0
        lineCounter = ((lineCounter+1) % numberOfrows)
    return data


def lowFreqShortWindow(filePath, isLongTimeWindow, shotTimeWindowPath):
    #if isLongTimeWindow == 1:#TODO find their threshold
     #   return [] #TODO assert this


    return
