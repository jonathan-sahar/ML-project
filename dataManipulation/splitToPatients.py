__author__ = 'Inspiron'

import csv
from utils.constants import *


def splitToPatients(outputDir = UNIFIED_TABLES_FOLDER):
    allLines = []
    dataFilePath = os.path.join(outputDir, "unified_table.csv")
    dataFile = open(dataFilePath, 'r')
    reader = csv.reader(dataFile)
    headers = reader.next()
    for row in reader:
        allLines.append(row)
    for patient in PATIENTS:
        print patient
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
    splitToPatients()