__author__ = 'Inspiron'


from datetime import datetime
import os
import csv
import re
import numpy as np
import scipy.stats as stats


CONTROL = ['APPLE', 'DAFODIL', 'LILLY', 'LILY', 'ORANGE', 'ROSE', 'SUNFLOWER', 'SWEETPEA']
UNDERLINES_BEFORE_NAME = 2
LONG_TIME_WINDOW = 300
SHORT_TIME_WINDOW = 5
delete = False


def addLabels(dirname, filenames):
    for fileName in filenames:
        filePath = os.path.join(dirname,fileName)

        # avoid junk files
        name, extension = os.path.splitext(filePath)
        if extension != ".csv" or fileName[0] == '.' or fileName[:7] == 'divided':
            continue
        # get subject's name with regex, check if sick or control
        match_exp = re.compile('([A-Z]+)')
        subject_name = match_exp.search(fileName).group(0)
        if subject_name in CONTROL:
            sick = 0
        else:
            sick = 1
        all_lines = []

        # open file for writing
        with open(filePath, 'r') as input_file:
            reader = csv.reader(input_file)
            row0 = reader.next()
            row0.append('Is sick')
            all_lines.append(row0)
            for row in reader:
                row.append(str(sick))
                all_lines.append(row)

        # open file for writing
        with open(filePath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(all_lines)

def createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, TimeWindow):
    for fileName in filenames:
        filePath = os.path.join(dirname,fileName)
        fileIntro, fileExtension = os.path.splitext(filePath)
        if fileName[0:9] == 'hdl_accel' and fileExtension == '.csv':
            aggregate(filePath, accelAggregatorsList, TimeWindow)
        if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
            aggregate(filePath, audioAggregatorsList, TimeWindow)


def aggregate(filePath, aggregators, TimeWindow):
    newFilePath = filePath[:-4]+'_'+TimeWindow+'.csv'
    newFile = open(newFilePath, 'w')

    if TimeWindow == 'short':
        dataTimeWindows = divideToWindows(filePath, SHORT_TIME_WINDOW)
    elif TimeWindow == 'long':
        dataTimeWindows = divideToWindows(filePath, LONG_TIME_WINDOW)
        shortTimeWindows = divideToWindows(filePath[:-4]+'_short.csv', LONG_TIME_WINDOW/SHORT_TIME_WINDOW)
    else: #TimeWindow == 'entire':
        dataTimeWindows = divideToWindows(filePath, '''files length''')
        shortTimeWindows = divideToWindows(filePath[:-4]+'_short.csv', '''files length'''/SHORT_TIME_WINDOW) #TODO does that really exist?
        longTimeWindows = divideToWindows(filePath[:-4]+'_long.csv', '''files length'''/LONG_TIME_WINDOW)

    for func in aggregators:
        if TimeWindow == 'short':
            result = func(dataTimeWindows)
        elif TimeWindow == 'long':
            result = func(dataTimeWindows, shortTimeWindows)
        else:
            result = func(dataTimeWindows, shortTimeWindows, longTimeWindows)
        #result is a matrix that every column calculates a feature
        appendColumn(newFile, result)

'''
def aggregate(dirname, fileName, aggregators, isLongTimeWindow, stringForName):
    filePath = os.path.join(dirname,fileName)
    dataFile = open(filePath)
    newFilePath = os.path.join(dirname,'divided'+fileName[3:-4]+'_'+stringForName+'.csv')
    newFile = open(newFilePath, 'w') #is it OK to pass a file?
    windows = []
    for func in aggregators:
        if isLongTimeWindow:
            windowLength = LONG_TIME_WINDOW
        else:
            windowLength = SHORT_TIME_WINDOW
        window =[]
        reader = csv.reader(dataFile)
        for i in range(0,windowLength):
            window.append(reader.next())
        windows.append(func(window))
        #result is a matrix that every column calculates a feature
        appendColumn(newFile, newFile, windows)
'''

def appendColumn(newFile, filePath, result):
    allLines = []
    reader = csv.reader(newFile)
    resultIter = iter(result)
    for row in reader:
        row+= resultIter.next()
        allLines.append(row)

        # open file for writing
        with open(filePath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(allLines)

#the three currently are not really needed. also, stringFoName not needed
def createShortTimeWindowTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, TimeWindow='short')


def createLongTimeWindowTable(dirname, filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, TimeWindow='long')


def createEntireTimeWindowTable(dirname, filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, TimeWindow='entire')


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


def stats(timeWindow, timeWindowLength):
    func_pointers = [(stats.tmax, 'max'), stats.tmin, stats.trim_mean] #TODO add more functions and tuple with feature name

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

'''
def calculateFeatureFromColumn(windows, functionsAndIndexs):
    #calculates each func with relevant
    return
'''

def lowFreqShortWindow(filePath, isLongTimeWindow, shotTimeWindowPath):
    #if isLongTimeWindow == 1:#TODO find their threshold
     #   return [] #TODO assert this


    return


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


if __name__ == "__main__":
    rootFolder = True
    accelAggregatorsListLong = []
    audioAggregatorsListLong = []
    accelAggregatorsListShort = []
    audioAggregatorsListShort = []
    accelAggregatorsListEntire = []
    audioAggregatorsListEntire = []
    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\FAKEDATA'):
        if rootFolder == True:
            rootFolder = False
            continue
        addLabels(dirname, filenames)
        createShortTimeWindowTable(dirname,filenames, accelAggregatorsListShort, audioAggregatorsListShort)
        createLongTimeWindowTable(dirname, filenames, accelAggregatorsListLong, audioAggregatorsListLong)
        createEntireTimeWindowTable(dirname, filenames, accelAggregatorsListEntire, audioAggregatorsListEntire)



'''
f = open(filePath, 'w')
            lines = []
            allLines =
            for line in allLines:
                #print "sometjons"
                if lineCounter == 0:
                    line += ',"Is sick"'
                    lines.append(line)
                    lineCounter+=1
                    continue
                line += ','+str(sick)
                lines.append(line)
            f.close()
            os.remove(filePath)
            f = open(filePath, 'w')
            print lines[0]
            f.writelines(lines)
            print f.readlines()[0]




def addLabels(dirname, filenames):
    for fileName in filenames:
        lineCounter = 0
        filePath = os.path.join(dirname,fileName)
        fileIntro, fileExtension = os.path.splitext(filePath)
        name = fileName
        underscoreCounter = 0
        if fileExtension == '.csv':
            while underscoreCounter < UNDERLINES_BEFORE_NAME:
                if name[0] == '_':
                    underscoreCounter += 1
                name = name[1:]
            if name[0:4] in ['Appl', 'Dafo', 'Lill', 'Lily', 'Oran', 'Rose', 'Sunf', 'Swee']:
                sick = 0
            else:
                sick = 1

            all_lines = []
            with open(filePath, 'r') as input_file:
                    reader = csv.reader(input_file)
                    row0 = reader.next()
                    #print row0
                    row0.append('Is sick')
                    #print row0
                    #print("appending".format(row0))
                    all_lines.append(row0)
                    for row in reader:
                        row.append(str(sick))
                        all_lines.append(row)
            with open(filePath, 'w') as out_file:
                writer = csv.writer(out_file, lineterminator='\n')
                writer.writerows(all_lines)
    return



'''
