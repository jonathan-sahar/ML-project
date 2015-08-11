__author__ = 'Inspiron'

from utils.constants import *
from utils.utils import *
from heapq import nlargest

#SCALED_UNIFIED_AGGREGATED_DATA_PATH
#UNIFIED_ENTIRE_DATA_PATH
#UNIFIED_AGGREGATED_DATA_PATH

def scaleColumn(values, isAggregated):
    oldMax = max(values)
    oldMin = min(values)

    if isAggregated:
        maxList = nlargest(20, range(0,len(values)), key=lambda i: values[i])
        oldMax = maxList[-1]
        mixList = nlargest(1, range(0,len(values)-20), key=lambda i: values[i])
        oldMin = mixList[-1]

    factor = 2.0/((oldMax - oldMin)+0.0000001)

    scaledList = []
    for value in values:
        scaledValue = (value - oldMin)*factor - 1.0

        if scaledValue > 1:
            scaledValue = 1
        if scaledValue < -1:
            scaledValue = -1

        scaledList.append(scaledValue)
    return scaledList

def scale(DATA_PATH, SCALED_DATA_PATH, isAggregated):
    entireData = readFileToFloat(DATA_PATH)
    # entireData = readFileToFloat('C:\ML\parkinson\orEstimation\unified_entire.csv')

    features = entireData.dtype.names
    scaledData = []

    for feature in features:
        values = entireData[feature]
        scaledValues = scaleColumn(values, isAggregated)
        scaledData.append(scaledValues)

    scaledDataArray = np.array(scaledData)
    scaledDataArray = scaledDataArray.T

    with open(SCALED_DATA_PATH, 'w') as file:
    # with open('C:\ML\parkinson\orEstimation\scaled_unified_entire.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(features)
        writer.writerows(scaledDataArray)

def scaleData():
    scale(UNIFIED_ENTIRE_DATA_PATH, SCALED_UNIFIED_ENTIRE_DATA_PATH, False)
    scale(UNIFIED_AGGREGATED_DATA_PATH, SCALED_UNIFIED_AGGREGATED_DATA_PATH, True)

if __name__=='__main__':
    scaleData()
