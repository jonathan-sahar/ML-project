__author__ = 'Inspiron'

import csv
from constants import *


if __name__ == "__main__":
    allLines = []
    #newFile = open(DATA_TABLE_FILE_PATH, 'r')
    #reader = csv.reader(newFile)
    #for row in reader:
    for row in open(DATA_TABLE_FILE_PATH, 'r').readlines():
        allLines.append(row)

    for patient in PATIENTS:
        patientLines = []
        shortAggregatedFile = open(DATA_TABLE_FILE_PATH[-4:]+'_'+patient+'.csv', 'w')
        for line in allLines:
            print line[28]
            if line[28] == patient: #TODO magic number :(
                patientLines.append(line)

        writer = csv.writer(shortAggregatedFile, lineterminator='\n') #TODO why would dataTable have \n in the end (also other places)
        writer.writerows(patientLines)