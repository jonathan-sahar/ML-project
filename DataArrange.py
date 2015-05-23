__author__ = 'Inspiron'

import os
import shutil
from datetime import datetime
from constants import *
import re
import csv


delete = False

def deleteUnvalidData(dirname, filenames):

    #both initiated to True in case they are not found in the folder at all
    isValidSecAccel = True
    isValidSecAudio = True
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
            (accelLines, isValidSecAccel, accelLineCounter) = validTable(26, filePath)
            #making sure there are not remain rows for aggregation
            del accelLines[-(accelLineCounter % LONG_TIME_WINDOW):]
        if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
            (audioLines, isValidSecAudio, audioLineCounter) = validTable(20, filePath)
            #making sure there are not remain rows for aggregation
            del audioLines[-(audioLineCounter % LONG_TIME_WINDOW):]
    #if isValidSecAccel or isValidSecAudio is false, the the data is 'foul'
    isFoulSec = not (isValidSecAccel and isValidSecAudio)
    lines = mergeLists(accelLines, audioLines)
    if (accelLineCounter <= LONG_TIME_WINDOW) or (audioLineCounter <= LONG_TIME_WINDOW) or (isFoulSec == True) \
            or ((accelLineCounter - accelLineCounter%LONG_TIME_WINDOW) != (audioLineCounter - audioLineCounter%LONG_TIME_WINDOW)):
            #or (accelStartTime != audioStartTime):
        if (delete == True) and (SubfolderCounter>0):
           shutil.rmtree(dirname)
        return ([], 0, accelLineCounter)
    else:
        return (lines, accelLineCounter, 0)

def mergeLists(leftList, rightList):

    all_lines = []
    rightListIter = iter(rightList)
    for line in leftList:
        all_lines.append((line+rightListIter.next()))
    return all_lines

def addLabels(dirname, filenames):
    for fileName in filenames:
        filePath = os.path.join(dirname,fileName)

        # avoid junk files
        name, extension = os.path.splitext(filePath)
        if extension != ".csv" or fileName[0] == '.' or fileName[:7] == 'divided':
            continue
        # get subject's name with regex, check if sick or control
        match_exp = re.compile('_([A-Z]+)_')
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
            row0.append('Patient')
            all_lines.append(row0)
            for row in reader:
                row.append(str(sick))
                row.append(subject_name)
                all_lines.append(row)

        # open file for writing
        with open(filePath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(all_lines)


def validTable(dateColumb, filePath):
    lineCounter = 0
    lines = []
    for line in open(filePath, 'r').readlines():
        #skip titles
        if lineCounter == 0:
            lineCounter+=1
            continue
        columns = line.split(',')
        try:
            dateObj = datetime.strptime(columns[dateColumb][0:19], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            #TODO delete line
            print "fuck"
            continue
        if lineCounter == 1:
            lastTime = dateObj
        if lineCounter == 2:
            twoLastTime = lastTime
            lastTime = dateObj
        if (dateObj - lastTime).seconds > 2 and (dateObj - twoLastTime).seconds > 2:
            return (False, lineCounter)
        twoLastTime = lastTime
        lastTime = dateObj
        lineCounter+=1
        lines.append(line)
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
        (table ,goodPart, badPart) = deleteUnvalidData(dirname, filenames)
        goodRecordings += goodPart
        badRecordings += badPart
        dataTable += table

    writer = csv.writer(dataFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
    writer.writerows(dataTable)

    print('time under 5 min is {}'.format(badRecordings))
    print('time over 5 min is {}'.format(goodRecordings))
    print(float(badRecordings)/(float(goodRecordings+1)))

