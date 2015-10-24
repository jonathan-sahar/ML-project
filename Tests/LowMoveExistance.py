__author__ = 'Inspiron'

import csv
from utils.constants import *

def lowMoveExistance(outputDir = UNIFIED_TABLES_FOLDER):
    dataFilePath = os.path.join(outputDir, "unified_table.csv")
    dataFile = open(dataFilePath, 'r')
    reader = csv.reader(dataFile)
    headers = reader.next()
    counter = 0
    print headers[58]
    for row in reader:
        print row[58]
        if row[58] < 0.01:
            counter = counter +1
    print "the counter "
    print counter


if __name__ == "__main__":
    lowMoveExistance()