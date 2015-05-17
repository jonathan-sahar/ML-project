__author__ = 'Inspiron'

import os
import shutil
from datetime import datetime

SHORT_TIME_WINDOW = 5
LONG_TIME_WINDOW = 300
delete = False

def main():
    goodRecordings = 0
    badRecordings = 0
    SubfolderCounter = 0
    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\DATA'):
        if SubfolderCounter == 0:
            #don't want to delete root
            SubfolderCounter+=1
            continue
        #both initiated to True in case they are not found in the folder at all
        isValidSecAccel = True
        isValidSecAudio = True
        for fileName in filenames:
            #going on all files in root and each subfolder
            filePath = os.path.join(dirname,fileName)
            fileIntro, fileExtension = os.path.splitext(filePath)
            if fileName[0:9] == 'hdl_accel' and fileExtension == '.csv':
                (isValidSecAccel, accelLineCounter) = validTable(26, filePath, 0)
                #making sure there are not remain rows for aggregation
                deleteLastRows(filePath, accelLineCounter % LONG_TIME_WINDOW)
            if fileName[0:9] == 'hdl_audio' and fileExtension == '.csv':
                (isValidSecAudio, audioLineCounter) = validTable(20, filePath, 0)
                #making sure there are not remain rows for aggregation
                deleteLastRows(filePath, accelLineCounter % LONG_TIME_WINDOW)
        #if isValidSecAccel or isValidSecAudio is false, the the data is 'foul'
        isFoulSec = not (isValidSecAccel and isValidSecAudio)
        if accelLineCounter <= LONG_TIME_WINDOW or audioLineCounter <= LONG_TIME_WINDOW or isFoulSec == True:
            badRecordings = badRecordings + accelLineCounter
            if (delete == True) and (SubfolderCounter>0):
               shutil.rmtree(dirname)
        else:
            goodRecordings = goodRecordings + accelLineCounter


    print('time under 5 min is {}'.format(badRecordings))
    print('time over 5 min is {}'.format(goodRecordings))
    print(float(badRecordings)/(float(goodRecordings+1)))

def deleteLastRows(filePath, numberOfLines):
    return

def validTable(dateColumb, filePath, lineCounter):
    for line in open(filePath, 'r').readlines():
        if lineCounter == 0:
            lineCounter+=1
            continue
        columbs = line.split(',')
        try:
            dateObj = datetime.strptime(columbs[dateColumb][0:19], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            #TO DO delete line
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
    return (True, lineCounter)

if __name__ == "__main__":
    main()

'''
NUMBER_OF_UNDERSCORES_BEFORE_DATE = 5
DATE_LENGTH = 8
YEAR_LENGTH = 4
NON_YEAR_TIEM_LENGTH = 2
TIME_LENGTH = 6

def numberOfCSV():
    for dirname in os.walk('C:\ML\parkinson\FAKEDATA'):
    # get path to all subdirectories first.
        for dirname, dirnames, filenames in os.walk("."):
            print "middle"
            for file in filenames:
                print file
        print 'end'
'''


'''
     callthecommandhere(blablahbla, filename, foo)
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # process arguments
    for arg in args:
        process(arg) # process() is defined elsewhere



    for dirname, dirnames, filenames in os.walk('C:\ML\parkinson\Data'):
    # get path to all subdirectories first.
        for subdirname in dirnames:
            name = subdirname
            print name
            counter = 0
            while counter < NUMBER_OF_UNDERSCORES_BEFORE_DATE:
                if name[0] == '_':
                    counter += 1
                name = name[1:]
            if name[0] == 'A' or 'u':
                while name[0] != '_':
                    name = name[1:]
                name = name[1:]

            startYear = int(name[0:YEAR_LENGTH])
            startMonth = int(name[YEAR_LENGTH:YEAR_LENGTH+NON_YEAR_TIEM_LENGTH])
            startDay = int(name[YEAR_LENGTH+NON_YEAR_TIEM_LENGTH:DATE_LENGTH])
            name = name[DATE_LENGTH+1:]
            startHour = int(name[0:NON_YEAR_TIEM_LENGTH])
            startMinute = int(name[NON_YEAR_TIEM_LENGTH:2*NON_YEAR_TIEM_LENGTH])
            startSecond = int(name[2*NON_YEAR_TIEM_LENGTH:TIME_LENGTH])
            name = name[TIME_LENGTH+1:]
            endYear = int(name[0:YEAR_LENGTH])
            endMonth = int(name[YEAR_LENGTH:YEAR_LENGTH+NON_YEAR_TIEM_LENGTH])
            endDay = int(name[YEAR_LENGTH+NON_YEAR_TIEM_LENGTH:DATE_LENGTH])
            name = name[DATE_LENGTH+1:]
            endHour = int(name[0:NON_YEAR_TIEM_LENGTH])
            endMinute = int(name[NON_YEAR_TIEM_LENGTH:2*NON_YEAR_TIEM_LENGTH])
            endSecond = int(name[2*NON_YEAR_TIEM_LENGTH:TIME_LENGTH])

            a = dt.datetime(startYear,startMonth,startDay,startHour,startMinute,startSecond)
            b = dt.datetime(endYear,endMonth,endDay,endHour,endMinute,endSecond)
            time = (b-a).total_seconds()

            if time >= FIVE_MINUTES:
                overFiveMinutesRecordings = overFiveMinutesRecordings + time
            else:
                underFiveMinutesRecordings = underFiveMinutesRecordings + time
    print('time under 5 min is {}'.format(underFiveMinutesRecordings))
    print('time over 5 min is {}'.format(overFiveMinutesRecordings))
'''