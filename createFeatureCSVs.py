__author__ = 'Inspiron'


from datetime import datetime
import os
import csv
import re
<<<<<<< HEAD
import numpy as np
import scipy.stats as stats
=======
import numpy
>>>>>>> origin/master

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

def createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, isLongTimeWindow, stringForName):
    for fileName in filenames:
        filePath = os.path.join(dirname,fileName)
        fileIntro, fileExtension = os.path.splitext(filePath)
        if fileName[0:9] == 'hdl_accel' and fileExtension == '.csv':
            aggregate(dirname, fileName, accelAggregatorsList, isLongTimeWindow, stringForName)
        if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
            aggregate(dirname, fileName, audioAggregatorsList, isLongTimeWindow, stringForName)


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


def appendColumn(newFile, filePath, result):
    allLines = []
    reader = csv.reader(newFile)
    resultIter = iter(result)
    for row in reader:
        row+= resultIter.next()
        allLines.append(row) #TODO I don't think append. all the columns in the same layer

        # open file for writing
        with open(filePath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(allLines)


def createShortTimeWindowTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, isLongTimeWindow=0, stringForName='short')


def createLongTimeWindowTable(dirname, filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, isLongTimeWindow=1, stringForName='long')


def stats(filePath, isLongTimeWindow, shotTimeWindowPath):

    func_pointers = [stats.tmax, stats.tmin, stats.trim_mean]
    if isLongTimeWindow == 0:
        return []
    data = []
    reader = csv.reader(filePath)
    for row in reader:
        data.append(row)
    data = np.array(data)
    for column in data.T:
        values = [func(column) for func in func_pointers]
    return values

def lowFreqShortWindow(filePath, isLongTimeWindow, shotTimeWindowPath):
    if isLongTimeWindow == 1:
        return [] #TODO assert this
    return


def lowFreqsCounter(window, shortTimeWindowPath):
    #if isLongTimeWindow == 0:
     #   return [] #TODO assert this
    numberOfrows = LONG_TIME_WINDOW/SHORT_TIME_WINDOW
    data = []
    shortTimeWindowFile = open(shortTimeWindowPath)
    reader = csv.reader(shortTimeWindowFile)
    dataIter = iter(reader)
    counter = 0
    for row in reader:
        counter = ((counter+1) % numberOfrows)
        data.append(row)
    data = np.array(data)
    for column in data.T:

    return


def mean(filePath, isLongTimeWindow, shotTimeWindowPath):
    return

if __name__ == "__main__":
    rootFolder = True
    accelAggregatorsList = []
    audioAggregatorsList = []
    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\FAKEDATA'):
        if rootFolder == True:
            rootFolder = False
            continue
        addLabels(dirname, filenames)
        createShortTimeWindowTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList)
        createLongTimeWindowTable(dirname, filenames, accelAggregatorsList, audioAggregatorsList)




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
