__author__ = 'Inspiron'

import os
import shutil
from datetime import datetime
from constants import *
from structuredDataConstants import accl_fields, audio_fields
import numpy as np
import re
import csv
from createFeatureCSVs import readFileAsIs, readFileToFloat


def deleteInvalidData(dirname, filenames):
    global subFolderCounter
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
            (accelLines, isValidAcclTable, accelLineCounter, acclHeader) = validTable(26, filePath)
            #making sure there are not remain rows for aggregation
            #del accelLines[-((accelLineCounter % LONG_TIME_WINDOW)-1):]

        if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
            (audioLines, isValidAudioTable, audioLineCounter, audioHeader) = validTable(20, filePath)
            #making sure there are not remain rows for aggregation
            #del audioLines[-((audioLineCounter % LONG_TIME_WINDOW)-1):]

    tablesContainGaps = not (isValidAcclTable and isValidAudioTable)
    (accelLines,audioLines) = makeSameStartTime(accelLines,audioLines)
    (accelLines,audioLines) = makeSameLength(accelLines,audioLines)
    if isValidAcclTable and isValidAudioTable:
        logger.debug("data length - after: {}, {}".format(len(accelLines), len(audioLines)))

    if (accelLineCounter <= LONG_TIME_WINDOW) or (tablesContainGaps == True):
        if (delete == True) and (subfolderCounter>0):
            shutil.rmtree(dirname)
        return ([], 0, accelLineCounter)
    else:
        headers = acclHeader[0] + audioHeader[0]
        _headers = [h.replace('.', '_') for h in headers]
        data = mergeLists(accelLines, audioLines)
        lines = [_headers] + data

        return (lines, accelLineCounter, 0)

def makeSameLength(accelLines,audioLines):
    newLength = min(len(accelLines),len(audioLines))
    newLength = newLength - newLength%LONG_TIME_WINDOW
    accelLines = accelLines[0:newLength]
    audioLines = audioLines[0:newLength]
    return (accelLines, audioLines)

def makeSameStartTime(accelLines,audioLines):
    if len(accelLines) < 4 or len(audioLines) < 4:
        return ([],[])
    accelLine = accelLines[1]
    audioLine = audioLines[1]
    acceldateObj = datetime.strptime(accelLine[26][0:19], '%Y-%m-%d %H:%M:%S')
    audiodateObj = datetime.strptime(audioLine[20][0:19], '%Y-%m-%d %H:%M:%S')
    while acceldateObj > audiodateObj:
        if len(audioLines) < 4:
            break
        audioLines = [audioLines[0]]+audioLines[2:]
        audioLine = audioLines[1]
        audiodateObj = datetime.strptime(audioLine[20][0:19], '%Y-%m-%d %H:%M:%S')
    while audiodateObj > acceldateObj:
        if len(audioLines) < 4:
            break
        accelLines = [accelLines[0]]+accelLines[2:]
        accelLine = accelLines[1]
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
        # avoid junk files
        filePath = os.path.join(dirname,fileName)
        name, extension = os.path.splitext(filePath)
        if extension != ".csv" or os.path.getsize(filePath) < 4000 or fileName[:9] != 'hdl_audio' or fileName[:7] == 'divided': #TODO improve files name
            continue

        # get subject's name using regex, check if sick or control
        match_exp = re.compile('([A-Z]+)')
        subject_name = match_exp.search(fileName).group(0)
        if subject_name in CONTROL:
            sick = 0
        else:
            sick = 1

        lines = []
        # open file for writing
        with open(filePath, 'r') as input_file:
            reader = csv.reader(input_file)
            # headers = reader.next()
            lines += ([row for row in reader])
            lines[0].extend(['Is sick','Patient'])
            [line.extend([str(sick), subject_name]) for line in lines[1:]]


        with open(filePath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(lines)

def validTable(dateColumn, filePath):
    #TODO: add the first row (fields) if it's the first call to validate
    valid = True
    fileHandle = open(filePath, 'r')
    reader = csv.reader(fileHandle)
    header = [reader.next()]

    lines = []
    lineCounter = 1

    for line in reader:
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
    if valid == False: # TODO: is it ok we return empty lines when valid?
        return ([], False, lineCounter, header)
    return (lines, True, lineCounter, header)

#TODO: finish re-writing, discuss logic
def _validTable(removeMe, filePath):
    valid = True
    if os.path.getsize(filePath) < 4000:
        return ([], False, 0)

    data = readFileToFloat(filePath)

    diffSecs = data['diffSecs']
    deltas_1 = zip(diffSecs[:-1], diffSecs[1:])
    deltas_2 = zip(diffSecs[:-2], diffSecs[2:])
    offByOne = np.array([(b - a > MAX_TIME_DIFF) for a,b in deltas_1])
    offByTwo = np.array([(b - a > MAX_TIME_DIFF) for a,b in deltas_2])
    if offByOne.any() or offByTwo.any():
        return ([], False, len(diffSecs))
    else:
        return (data, True, len(diffSecs))


def arrangeData(rootDir = ROOT_DATA_FOLDER, outputDir = UNIFIED_TABLES_FOLDER):
    try:
        os.mkdir(outputDir)
    except WindowsError:
        pass
    goodRecordings = 0
    badRecordings = 0
    global subfolderCounter
    subfolderCounter = 0 # TODO: eliminate need for global
    dataTable = []

    for dirname, dirnames, filenames in os.walk(rootDir):
        if subfolderCounter == 0:
            #don't want to delete root
            subfolderCounter+=1
            continue
        #adding labels
        addLabels(dirname, filenames)
        #delete unwanted parts (bad table, and modulu of tables)
        (table ,goodPart, badPart) = deleteInvalidData(dirname, filenames)
        goodRecordings += goodPart
        badRecordings += badPart
        dataTable += table
    dataFilePath = os.path.join(outputDir, "unified_table.csv")
    dataFile = open(dataFilePath, 'w')
    writer = csv.writer(dataFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
    writer.writerows(dataTable)
    dataFile.close()

if __name__ == "__main__":
    arrangeData()

'''
rows = []
writePath = 'D:\Documents\Technion - Bsc Computer Science\ML Project\data_sample\HumDynLog_APPLE_LGE_LGE_A0000028AF9C96_20111220_115329_20111220_120000\out_test.csv'
dataFile = open(dirname + '\\' + filenames[0], 'r')
outFile = open(writePath, 'w')
reader = csv.reader(dataFile)
writer = csv.writer(outFile)
for row in reader:
    rows.append(row)

writer.writerows(rows)
'''
