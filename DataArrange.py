__author__ = 'Inspiron'

import os
import shutil
from datetime import datetime
from constants import *
import numpy as np
import re
import csv




def deleteInvalidData(dirname, filenames):
    delete = False
    #both initiated to True in case they are not found in the folder at all
    isValidAcclTable = True
    isValidAudioTable = True
    accelLineCounter = 0
    audioLineCounter = 0
    #accelStartTime = None
    #audioStartTime = None
    accelLines = []
    audioLines = []

    for fileName in filenames:
        #going on all files in current folder
        filePath = os.path.join(dirname,fileName)
        fileIntro, fileExtension = os.path.splitext(filePath)
        if fileName[0:9] == 'hdl_accel' and fileExtension == '.csv':
            print 'processing accl'
            (accelLines, isValidAcclTable, accelLineCounter) = validTable(26, filePath)
            #making sure there are not remain rows for aggregation
            #del accelLines[-((accelLineCounter % LONG_TIME_WINDOW)-1):]
            #print "after accel"
            #print(len(accelLines))
        if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
            print 'processing audio'
            (audioLines, isValidAudioTable, audioLineCounter) = validTable(20, filePath)
            #making sure there are not remain rows for aggregation
            #print "be  fore audio"
            #print len(audioLines)
            #del audioLines[-((audioLineCounter % LONG_TIME_WINDOW)-1):]
            #print "after audio"
            #print len(audioLines)
    #if isValidAcclTable or isValidAudioTable is false, the the data is 'foul'
    tablesContainGaps = not (isValidAcclTable and isValidAudioTable)
    (accelLines,audioLines) = makeSameStartTime(accelLines,audioLines)
    (accelLines,audioLines) = makeSameLength(accelLines,audioLines)
    print "printing from deleteInvalidData:"
    # print accelLines
    # print audioLines

    if (accelLineCounter <= LONG_TIME_WINDOW) or (tablesContainGaps == True):
        if (delete == True) and (SubfolderCounter>0):
           shutil.rmtree(dirname)
        return ([], 0, accelLineCounter)
    else:
        lines = mergeLists(accelLines, audioLines)
        return (lines, accelLineCounter, 0)

def makeSameLength(accelLines,audioLines):
    newLength = min(len(accelLines),len(audioLines))
    newLength = newLength - newLength%LONG_TIME_WINDOW + 1
    accelLines = accelLines[0:newLength]
    audioLines = audioLines[0:newLength]
    return (accelLines, audioLines)

def makeSameStartTime(accelLines,audioLines):
    if len(accelLines) < 2 or len(audioLines) < 2:
        return ([],[])
    accelLine = accelLines[1]
    audioLine = audioLines[1]
    acceldateObj = datetime.strptime(accelLine[26][0:19], '%Y-%m-%d %H:%M:%S')
    audiodateObj = datetime.strptime(audioLine[20][0:19], '%Y-%m-%d %H:%M:%S')
    while acceldateObj > audiodateObj:
        audioLines = [audioLines[0]]+audioLines[2:]
        audioLine = audioLines[1]
        audiodateObj = datetime.strptime(audioLine[20][0:19], '%Y-%m-%d %H:%M:%S')
    while audiodateObj > acceldateObj:
        accelLines = [accelLines[0]]+accelLines[2:]
        accelLine = (accelLines[1]).split(',')
        acceldateObj = datetime.strptime(accelLine[26][0:19], '%Y-%m-%d %H:%M:%S')
    return (accelLines,audioLines)

def mergeLists(leftList, rightList):
    all_lines = []
    rightListIter = iter(rightList)
    for line in leftList:
        all_lines.append((line+rightListIter.next()))
    return all_lines

def addLabels(dirname, filenames):
    for fileName in filenames:
        filePath = os.path.join(dirname,fileName)
        outPath = os.path.join(dirname,'output.csv')
        # avoid junk files
        name, extension = os.path.splitext(filePath)
        if extension != ".csv" or fileName[0:9] != 'hdl_audio' or fileName[:7] == 'divided':
            continue
        # get subject's name with regex, check if sick or control
        match_exp = re.compile('([A-Z]+)')
        subject_name = match_exp.search(fileName).group(0)
        if name in CONTROL:
            sick = 0
        else:
            sick = 1
        all_lines = []

        # open file for writing
        with open(filePath, 'r') as input_file:
            reader = csv.reader(input_file)
            row0 = reader.next()
            row0.append('Is sick')
            row0.append('Patient')
            all_lines.append(row0)
            for row in reader:
                row.append(str(sick))
                row.append(subject_name[1:-1])
                all_lines.append(row)

        # open file for writing
        with open(outPath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(all_lines)


def validTable(dateColumn, filePath):
#TODO: add the first row (fields) if it's the first call to validate
    valid = True
    lineCounter = 0
    lines = []
    fileHandle = open(filePath, 'r')
    reader = csv.reader(fileHandle)

    for line in reader:
        #skip titles
        if lineCounter == 0:
            lineCounter+=1
            continue
        try:
            dateObj = datetime.strptime(line[dateColumn], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue
        if lineCounter == 1:
            lastTime = dateObj
        if lineCounter == 2:
            twoLastTime = lastTime
            lastTime = dateObj
        if (dateObj - lastTime).seconds > 2 and (dateObj - twoLastTime).seconds > 2:
            valid = False
        twoLastTime = lastTime
        lastTime = dateObj
        lineCounter+=1
        lines.append(line)

    if valid == False:
        return ([], False, lineCounter)
    return (lines, True, lineCounter)

if __name__ == "__main__":


    dataFile = open(DATA_TABLE_FILE_PATH, 'w')
    goodRecordings = 0
    badRecordings = 0
    SubfolderCounter = 0
    dataTable = []

    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\FAKEDATA'):
        if SubfolderCounter == 0:
            #don't want to delete root
            SubfolderCounter+=1
            continue
        #adding labels
        addLabels(dirname, filenames)
        #delete unwanted parts (bad table, and modulu of tables)
        (table ,goodPart, badPart) = deleteInvalidData(dirname, filenames)
        goodRecordings += goodPart
        badRecordings += badPart
        dataTable += table

    writer = csv.writer(dataFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
    writer.writerows(dataTable)
    dataFile.close()

    print('time to delete {}'.format(badRecordings))
    print('time to remain {}'.format(goodRecordings))
    print 'percentage to delete'+str((float(badRecordings)/(float(goodRecordings+badRecordings))))


'''
rows = []
writePath = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\HumDynLog_APPLE_LGE_LGE_A0000028AF9C96_20111220_115329_20111220_120000\out_test.csv'
dataFile = open(dirname + '\\' + filenames[0], 'r')
outFile = open(writePath, 'w')
reader = csv.reader(dataFile)
writer = csv.writer(outFile)
for row in reader:
    rows.append(row)
print rows
writer.writerows(rows)
'''
