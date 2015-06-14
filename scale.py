__author__ = 'Inspiron'

from constants import *
from utils import *
import csv
import numpy as np

#SCALED_UNIFIED_AGGREGATED_DATA_PATH
#UNIFIED_ENTIRE_DATA_PATH
#UNIFIED_AGGREGATED_DATA_PATH

def scaleColumn(values):
    oldMax = max(values)
    oldMin = min(values)
    factor = 1.0/(oldMax - oldMin)

    scaledList = []
    for value in values:
        scaledValue = (value - oldMin)*factor
        scaledList.append(scaledValue)
    return scaledList

def scale(DATA_PATH, SCALED_DATA_PATH):
    #entireData = readFileToFloat(DATA_PATH)
    entireData = readFileToFloat('C:\ML\parkinson\orEstimation\unified_entire.csv')

    features = entireData.dtype.names
    scaledData = []

    for feature in features:
        values = entireData[feature]
        print values
        scaledValues = scaleColumn(values)
        scaledData.append(scaledValues)
    print scaledData

    scaledDataArray = np.array(scaledData)
    scaledDataArray = scaledDataArray.T

    #with open(SCALED_DATA_PATH, 'w') as file:
    with open('C:\ML\parkinson\orEstimation\scaled_unified_entire.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(features)
        writer.writerows(scaledDataArray)

if __name__=='__main__':
    scale(UNIFIED_ENTIRE_DATA_PATH, SCALED_UNIFIED_ENTIRE_DATA_PATH)
    scale(UNIFIED_AGGREGATED_DATA_PATH, SCALED_UNIFIED_AGGREGATED_DATA_PATH)