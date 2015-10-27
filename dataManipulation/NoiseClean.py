__author__ = 'Inspiron'


import csv
import utm
import numpy as np
from utils.utils import *
from utils.constants import *
from dataManipulation.createFeatureCSVs import divideToWindows


import pdb
def maxSpeed(gpsLocations):
    fastest = 0 #Meters per sec
    counter = 1
    totalTime = 0
    for (timediff, lat, long) in gpsLocations:
        #
        if counter == 1:
            (prevEasting,prevNorthing) = (lat, long)
        #
        if counter == 10:
            counter = counter+1
            totalTime = totalTime+timediff
            continue
        if counter == 10:
            totalTime = totalTime+timediff
            (easting, northing, zoneNumber, zoneLetter) = utm.from_latlon(lat, long)
            distance = np.sqrt((easting-prevEasting)^2 + (northing-prevNorthing)^2)
            speed = distance/totalTime #Meters per sec
            counter = 1
            if speed > fastest:
                fastest = speed
            #for debug only
            if speed > 0:
                print "non zero speed "
                print speed
            #end debug only
    return fastest


def deviceLayed():
    return


def deleteGPSNoise(patientLines):
    print "in deleteGPSNoise"
    cleanPatientLines = []
    locations = []
    deviceLayedIndicators = []
    windowNumberDbg = 0
    timeWindows = divideToWindows(patientLines, LONG_TIME_WINDOW) #TODO save a side the header
    for timeWindow in timeWindows:
        windowNumberDbg = windowNumberDbg+1 #for debug
        for line in timeWindow:
            #print line
            locations.append((line[60], line[61], line[62])) #change to relevant format (timediff, lat, long)
        fastest = maxSpeed(locations)
        isLayed = deviceLayed()
        #for debug only
        if fastest >= 9:
            print "the fastest movement "
            print fastest
            print "in window number "
            print windowNumberDbg
        #end of debug only
        if (fastest < 9) or (isLayed == True): #9 Meters per sec
            cleanPatientLines = cleanPatientLines + timeWindow
    return cleanPatientLines



def cleanNoise(outputDir = UNIFIED_TABLES_FOLDER):


    for patient in PATIENTS:
    #	pdb.set_trace()
        patientFilePath = os.path.join(outputDir, "DATAFILE_" + patient + ".csv")
        #patientLines = readFileAsIs(patientFilePath)
        #header = patientLines[0]
	print("reading patient file for {}...".format(patient))
        patientData = readFileToFloat(patientFilePath)
        header = np.array(patientData.dtype.names).tolist()
        patientLines = castStructuredArrayToRegular(patientData)
        patientLines = patientLines.tolist() #cast to list of list

        patientLines = deleteGPSNoise(patientLines)

        #print len(header)
        #print len(patientLines)
        #print len(patientLines[0])

        patientLines = [header] + patientLines
        patientFile = open(patientFilePath, 'w')
        writer = csv.writer(patientFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
        writer.writerows(patientLines)
        patientFile.close()

if __name__ == "__main__":
    cleanNoise()
