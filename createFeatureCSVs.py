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


def aggregate(DataMatrix, aggregators, TimeWindow):
    newFilePath
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
        #result is a matrix where every column is a calculated feature
        appendColumns(newFilePath, result)

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

def appendColumns(newFilePath, coloumns):
    """Do some things.
    :param newFile: path of file we want to append to.
    :param coloumns: matrix of calculated values to be appended (joined along the columns on the right)
    """
    allLines = []
    newFile = open(newFilePath, 'r')
    reader = csv.reader(newFile)
    resultIter= iter(coloumns)
    for row in reader:
        row += resultIter.next()
        allLines.append(row)

    # open file for writing
    with open(newFilePath, 'w') as out_file:
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


BLOCK_LENGTH = 1000 # TODO: set this to 1GB/sizeof(line)
DATA_TABLE_PATH = 'C:\ML\parkinson\FAKEDATA'
SHORT_TABLE_PATH = 'C:\ML\parkinson\FAKEDATA'
LONG_TABLE_PATH = 'C:\ML\parkinson\FAKEDATA'


if __name__ == "__main__":
    rootFolder = True
    accelAggregatorsListLong = []
    audioAggregatorsListLong = []
    accelAggregatorsListShort = []
    audioAggregatorsListShort = []
    accelAggregatorsListEntire = []
    audioAggregatorsListEntire = []

    block = []
    block_short = []
    num_lines = 0
    reader = csv.reader(DATA_TABLE_PATH)
    reader_short = csv.reader(SHORT_TABLE_PATH)
    append_short = True
    for row in reader:
        block.append(row)
        #try adding a line from the short windows file.
        if append_short:
            try:
                block_short.append(reader_short.next())
            except StopIteration:
                append_short = False
        num_lines += 1
        if num_lines == BLOCK_LENGTH:
            createShortTimeWindowTable(block, aggregatorsListShort)
            createLongTimeWindowTable(block,shortTimeMatrix, aggregatorsListLong)
            block = []
            num_lines = 0

    # rest of file, if no. of lines % BLOCK_LENGTH != 0
    createShortTimeWindowTable(block, aggregatorsListShort)
    createLongTimeWindowTable(block,shortTimeMatrix, aggregatorsListLong)
    createEntireTimeWindowTable(block, shortTimeMatrix, longTimeMatrix, aggregatorsListEntire)
    block = []
    num_lines = 0

    createEntireTimeWindowTable(block, shortTimeMatrix, longTimeMatrix, aggregatorsListEntire)

    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\FAKEDATA'):
        if rootFolder == True:
            rootFolder = False
            continue
        addLabels(dirname, filenames)


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
