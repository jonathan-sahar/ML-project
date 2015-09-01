__author__ = 'Inspiron'


import csv
from utils.constants import *
import utm
import numpy as np

def maxSpeed(gpsLocations):
    fastest = 0 #Meters per sec
    counter = 1
    (prevEasting,prevNorthing, prevZoneNumber, prevZoneLetter) = utm.from_latlon(gpsLocations[0])

    for gpsLocation in gpsLocations:
        #ten lines are approx 10 secs
        if counter < 10:
            counter = counter+1
            continue

        (easting, northing, zoneNumber, zoneLetter) = utm.from_latlon(gpsLocation)
        distance = np.sqrt((easting-prevEasting)^2 + (northing-prevNorthing)^2)
        speed = distance/10
        if speed > fastest:
            fastest = speed
        (prevEasting,prevNorthing) = (easting, northing)
        counter = 1
    return fastest


def findGPSNoise(gpsFileName, isExistGPSTable):
    gpsLocations = []#read GPSTable
    fastest = maxSpeed(gpsLocations)
    if fastest > 3: #Meters per sec:
        return True
    return False


def cleanNoise(outputDir = UNIFIED_TABLES_FOLDER):
    allLines = []
    dataFilePath = os.path.join(outputDir, "unified_table.csv")
    dataFile = open(dataFilePath, 'r')
    reader = csv.reader(dataFile)
    headers = reader.next()

    print "make sure these are headers: "
    print headers

    for row in reader:
        allLines.append(row)

    for patient in PATIENTS:
        patientLines = [headers]
        patientFilePath = os.path.join(outputDir, "DATAFILE_" + patient + ".csv")
        patientFile = open(patientFilePath, 'w')
        for line in allLines:
            if line[NUM_OF_BASIC_FEATURES-1] == patient:
                patientLines.append(line)
        writer = csv.writer(patientFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
        writer.writerows(patientLines)
        patientFile.close()
    dataFile.close()

if __name__ == "__main__":
    cleanNoise()