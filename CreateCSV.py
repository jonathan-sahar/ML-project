__author__ = 'Inspiron'

from datetime import datetime
import os
import csv
import re

CONTROL = ['APPLE', 'DAFODIL', 'LILLY', 'LILY', 'ORANGE', 'ROSE', 'SUNFLOWER', 'SWEETPEA']
UNDERLINES_BEFORE_NAME = 2
FIVE_MINUTES = 300
delete = False


def addLabels(dirname, filenames):
    for fileName in filenames:
        filePath = os.path.join(dirname,fileName)

        # avoid junk files
        name, extension = os.path.splitext(filePath)
        if extension != ".csv" or fileName[0] == '.':
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
    return

def aggregate(dirname, fileName, aggregators, isContext, stringForName):
    filePath = os.path.join(dirname,fileName)
    newFilePath = os.path.join(dirname,fileName[:-4]+'_'+stringForName+'.csv')
    f = open(newFilePath, 'w')
    for func in aggregators:
        if isContext == False:
            result = func(filePath, newFilePath, isContext)
        else:
            result = func(filePath, newFilePath, isContext, os.path.join(dirname,fileName[:-4]+'_short.csv'))
        #result is a matrix that every column calculates a feature
        appendColumn(newFilePath, result)

def appendColumn():

    return

def createShortTimeWindowTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, isLongTimeWindow=0, stringForName='short')
    return

def createLongTimeWindowTable(dirname, filenames, accelAggregatorsList, audioAggregatorsList):
    createAggregatedTable(dirname,filenames, accelAggregatorsList, audioAggregatorsList, isLongTimeWindow=1, stringForName='long')
    return

if __name__ == "__main__":
    rootFolder = True
    accelAggregatorsList = []
    audioAggregatorsList = []
    data_directory = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample'
    for dirname, dirnames, filenames in os.walk(data_directory):
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