__author__ = 'Inspiron'

import shutil
from datetime import datetime

from utils.constants import *
from utils.utils import *
#from geopy.distance import *

def deleteInvalidData(dirname, filenames, includeHeaders):
    global subFolderCounter
    delete = False
    #both initiated to True in case they are not found in the folder at all
    isValidAcclTable = True
    isValidAudioTable = True
    isValidCmpssTable = True
    isExistGPSTable = False
    accelLineCounter = 0
    audioLineCounter = 0
    cmpssLineCounter = 0
    #accelStartTime = None
    #audioStartTime = None
    accelLines = []
    audioLines = []
    cmpssLines = []
    gpsLines = []
    gpsFileName = None

    for fileName in filenames:
        #going on all files in current folder
        filePath = os.path.join(dirname,fileName)
        fileIntro, fileExtension = os.path.splitext(filePath)
        if fileName[0:9] == 'hdl_accel' and fileExtension == '.csv':
            (accelLines, isValidAcclTable, accelLineCounter, acclHeader) = validTable(26, filePath)

        if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
            (audioLines, isValidAudioTable, audioLineCounter, audioHeader) = validTable(20, filePath)

        if fileName[0:9] == 'hdl_cmpss' and fileExtension == '.csv':
            (cmpssLines, isValidCmpssTable, cmpssLineCounter, cmpssHeader) = validTable(14, filePath)

        if fileName[0:7] == 'hdl_gps' and fileExtension == '.csv':
            isExistGPSTable = True
            #TODO not disqualafy for GPS defected line, but just read the file
            lines = readFileAsIs(filePath)
            gpsHeader = lines[0]
            gpsLines = lines[1:]

    tablesContainGaps = not (isValidAcclTable and isValidAudioTable and isValidCmpssTable)
    (accelLines, audioLines, cmpssLines) = makeSameStartTime(accelLines,audioLines, cmpssLines) #TODO can add also GPS
    (accelLines, audioLines, cmpssLines, gpsLines) = makeSameLength(accelLines,audioLines, cmpssLines, gpsLines)

    #if isValidAcclTable and isValidAudioTable:
    #    logger.debug("data length - after: {}, {}".format(len(accelLines), len(audioLines)))

    if (len(accelLines) <= LONG_TIME_WINDOW) or (tablesContainGaps == True) or (isExistGPSTable == False):
        if (delete == True) and (subfolderCounter>0):
            shutil.rmtree(dirname)
        return ([], 0, accelLineCounter)
    else:
        #addPrefixToFeatures(acclHeader , audioHeader, cmpssHeader)
        headers = acclHeader[0] + audioHeader[0] + cmpssHeader[0] + gpsHeader
        _headers = [h.replace('.', '_') for h in headers]
        data = mergeLists(accelLines, audioLines, cmpssLines, gpsLines)
        if includeHeaders == True:
            lines = [_headers] + data
        else:
            lines = data

        return (lines, accelLineCounter, 0)

#def addPrefixToFeatures(acclHeader , audioHeader, cmpssHeader):
 #   for name in acclHeader[0]:
 #       name = "accel_"+name
 #   return

def makeSameLength(accelLines, audioLines, cmpssLines, gpsLines):
    newLength = min(len(accelLines),len(audioLines), len(cmpssLines), len(gpsLines))
    newLength = newLength - newLength%LONG_TIME_WINDOW
    accelLines = accelLines[0:newLength]
    audioLines = audioLines[0:newLength]
    cmpssLines = cmpssLines[0:newLength]
    gpsLines = gpsLines[0:newLength]
    return (accelLines, audioLines, cmpssLines, gpsLines)

def makeSameStartTime(accelLines,audioLines, cmpssLines):
    if len(accelLines) < 4 or len(audioLines) < 4 or len(cmpssLines) < 4:
        return ([], [], [])
    accelLine = accelLines[1]
    audioLine = audioLines[1]
    cmpssLine = cmpssLines[1]
    acceldateObj = datetime.strptime(accelLine[26][0:19], '%Y-%m-%d %H:%M:%S')
    audiodateObj = datetime.strptime(audioLine[20][0:19], '%Y-%m-%d %H:%M:%S')
    cmpssdateObj = datetime.strptime(cmpssLine[14][0:19], '%Y-%m-%d %H:%M:%S')

    #making sure audio doesn't start before accel
    (audioLines, audiodateObj) = alignRightToLeft(acceldateObj, audioLines, audiodateObj, 20)
    #making sure cmpss dosn't start before audio (and accel)
    (cmpssLines, cmpssdateObj) = alignRightToLeft(audiodateObj, cmpssLines, cmpssdateObj, 14)
    #making sure accel doesn't start before cmpss
    (accelLines, acceldateObj) = alignRightToLeft(cmpssdateObj, accelLines, acceldateObj, 26)
    #making sure audio doesn't start before modified accel
    (audioLines, audiodateObj) = alignRightToLeft(acceldateObj, audioLines, audiodateObj, 20)

    return (accelLines,audioLines,cmpssLines)

#making sure the right list doesn't start before the left obj
def alignRightToLeft(leftdateObj, rightList, rightdateObj, rightDateColumn):
    while leftdateObj > rightdateObj:
        if len(rightList) < 4:
            break
        rightList = [rightList[0]]+rightList[2:]
        rightFirstLine = rightList[1]
        rightdateObj = datetime.strptime(rightFirstLine[rightDateColumn][0:19], '%Y-%m-%d %H:%M:%S')
    return (rightList, rightdateObj)

def mergeLists(firstList, secondList, thirdList, fourthList):
    all_lines = []
    secondListIter = iter(secondList)
    thirdListIter = iter(thirdList)
    fourthListIter = iter(fourthList)
    for line in firstList:
        all_lines.append((line+secondListIter.next()+ thirdListIter.next()+ fourthListIter.next()))
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
            if lines[0][-1] != 'Patient':
                lines[0].extend(['Is sick','Patient'])
                [line.extend([str(sick), subject_name]) for line in lines[1:]]


        with open(filePath, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator='\n')
            writer.writerows(lines)

def validTable(dateColumn, filePath):
    #print filePath
    #TODO: add the first row (fields) if it's the first call to validate
    valid = True
    fileHandle = open(filePath, 'r')
    reader = csv.reader(fileHandle)
    header = [reader.next()]
    #print header
    lines = []
    lineCounter = 1

    for line in reader:
        try:
            dateObj = datetime.strptime(line[dateColumn][0:19], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue
        if lineCounter == 1:
            lastTime = dateObj
        if lineCounter == 2:
            twoLastTime = lastTime
            lastTime = dateObj
        if (dateObj - lastTime).seconds > 100 and (dateObj - twoLastTime).seconds > 100:
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
    #except WindowsError:
    except OSError:
        pass
    goodRecordings = 0
    badRecordings = 0
    global subfolderCounter
    subfolderCounter = 0 # TODO: eliminate need for global
    dataTable = []
    includeHeaders = True
    for dirname, dirnames, filenames in os.walk(rootDir):
        if subfolderCounter == 0:
            #don't want to delete root
            subfolderCounter = subfolderCounter+1
            continue
        #adding labels
        addLabels(dirname, filenames)
        #delete unwanted parts (bad table, and modulu of tables)
        (table ,goodPart, badPart) = deleteInvalidData(dirname, filenames, includeHeaders)
        if len(table) > 0:
            includeHeaders = False

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
