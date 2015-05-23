__author__ = 'Inspiron'

import csv
from constants import *


if __name__ == "__main__":
    allLines = []
    newFile = open(DATA_TABLE_FILE_PATH, 'r')
    reader = csv.reader(newFile)
    for row in reader:
        allLines.append(row)

    for patient in PATIENTS:
        shortAggregatedFile = open(DATA_TABLE_FILE_PATH+'_'+patient, 'w')
        for line in allLines:
            if line[] == patient:
