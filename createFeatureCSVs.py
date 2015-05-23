__author__ = 'Inspiron'
import os
import csv
import re
from constants import *
from featureCalculationFunctions import *



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
'''
   if TimeWindow == 'short':
        dataTimeWindows = divideToWindows(DataMatrix, SHORT_TIME_WINDOW)
    elif TimeWindow == 'long':
        dataTimeWindows = divideToWindows(DataMatrix, LONG_TIME_WINDOW)
        shortTimeWindows = divideToWindows(shortTimeMatrix, LONG_TIME_WINDOW/SHORT_TIME_WINDOW)
    else: #TimeWindow == 'entire':
        dataTimeWindows = divideToWindows(DataMatrix, DATA_SIZE)
        shortTimeWindows = divideToWindows(shortTimeMatrix, DATA_SIZE/SHORT_TIME_WINDOW) #TODO does that really exist?
        longTimeWindows = divideToWindows(longTimeMatrix, DATA_SIZE/LONG_TIME_WINDOW)
'''

def aggregate(aggregators, timeWindow, windowType, shortTimeWindows = None, longTimeWindows = None):

    for func in aggregators:
        if windowType == 'short':
            result = func(timeWindow)
        elif windowType == 'long':
            result = func(timeWindow, shortTimeWindows, windowType)
        else: # windowType = entire
            result = func(timeWindow, longTimeWindows, windowType)
        #result is a matrix where every column is a calculated feature
        return result
        #appendColumns(TimeWindow, result)


def appendColumns(TimeWindow, coloumns):
    """Do some things.
    :param TimeWindow: lets you know what's the file we want to append to.
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


def createShortTimeWindowTable(timeWindows, aggregatorsListShort):
    for timeWindow in timeWindows:
        result = aggregate(aggregatorsListShort, 'short', timeWindow, None, None)
        appendColumns()

def createLongTimeWindowTable(shortTimeWindows, longTimeWindows, aggregatorsListLong):
    for timeWindow in (shortTimeWindows,longTimeWindows): #TODO assert they are the same length
        aggregate(aggregatorsListLong, 'long', shortTimeWindows, longTimeWindows)

def createEntireTimeWindowTable(shortTimeWindows, entireTimeWindows, aggregatorsListEntire):
    for timeWindow in (shortTimeWindows,entireTimeWindows): #TODO assert they are the same length
        aggregate(aggregatorsListEntire, 'entire', shortTimeWindows, entireTimeWindows)


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


'''
def calculateFeatureFromColumn(windows, functionsAndIndexs):
    #calculates each func with relevant
    return
'''


def readFile():
    return

def divideToPatients(shortTimeWindows, longTimeWindows):
    return

if __name__ == "__main__":
    #define the aggregators for each table
    aggregatorsListLong = []
    aggregatorsListShort = []
    aggregatorsListEntire = []

    #creating the files in the path
    open(SHORT_TABLE_FILE_PATH).close()
    open(LONG_TABLE_FILE_PATH).close()
    open(ENTIRE_TABLE_FILE_PATH).close()

    #create 5 sec per line table
    dataMatrix = readFile(DATA_TABLE_FILE_PATH)
    shortTimeWindows  = divideToWindows(dataMatrix, SHORT_TIME_WINDOW)
    createShortTimeWindowTable(shortTimeWindows, aggregatorsListShort) #TODO check if easy to return the table

    #create 5 min per line table
    ShortWindowsMatrix = readFile(SHORT_TABLE_FILE_PATH)
    longTimeWindows = divideToWindows(ShortWindowsMatrix, LONG_TIME_WINDOW/SHORT_TIME_WINDOW)
    createLongTimeWindowTable(shortTimeWindows, longTimeWindows, aggregatorsListShort)

    #create patient per line table
    LongWindowsMatrix = readFile(LONG_TABLE_FILE_PATH)
    patientWindowsList = divideToPatients(dataMatrix, LongWindowsMatrix)
    for (patientShortWindow,patientEntireWindow) in patientWindowsList:
        createEntireTimeWindowTable(patientShortWindow, patientEntireWindow)


'''
    rootFolder = True

    dataMatrix = []
    shortTimeMatrix = []
    longTimeMatrix = []
    #TODO addLabels
    #TODO addLabels should move to foulDataDelete
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
    #TODO if I understand you code correctly, we're not suppose to have modulu. better assert that
    createShortTimeWindowTable(block, aggregatorsListShort)
    createLongTimeWindowTable(block,shortTimeMatrix, aggregatorsListLong)
    createEntireTimeWindowTable(block, shortTimeMatrix, longTimeMatrix, aggregatorsListEntire)
    block = []
    num_lines = 0

    createEntireTimeWindowTable(block, shortTimeMatrix, longTimeMatrix, aggregatorsListEntire)
'''
'''
    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\FAKEDATA'):
        if rootFolder == True:
            rootFolder = False
            continue
        addLabels(dirname, filenames)
        createShortTimeWindowTable(dataMatrix, AggregatorsListShort)
        createLongTimeWindowTable(dataMatrix,shortTimeMatrix, AggregatorsListLong)
        createEntireTimeWindowTable(dataMatrix, shortTimeMatrix, longTimeMatrix, AggregatorsListEntire)
'''


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
