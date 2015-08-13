__author__ = 'Inspiron'
import numpy.lib.recfunctions as nprf

from featureCalculationFunctions import *
from utils.utils import *


def aggregate(aggregators, windowType, dataWindow, aggregatedWindows):
    '''
    :param aggregators:
    :param windowType:
    :param dataWindow:
    :param aggregatedWindows:
    :return: headers: the list of headers matching output of all functions in aggregators
    :return: aggregatedWindow: the line of values generated by the aggregators for this time window.
    '''
    headers = []
    aggregatedWindow = np.atleast_2d([])
    for func in aggregators:
        if windowType == 'short':
            header, data = func(dataWindow)
        elif windowType == 'long':
            header, data = func(dataWindow, aggregatedWindows)
        else: #windowType == 'entire'
            header, data = func(dataWindow, aggregatedWindows, 'entire')
        headers.extend(header)
        aggregatedWindow = np.hstack((aggregatedWindow, np.atleast_2d(data)))
    return headers, aggregatedWindow

def createTimeWindowTable(aggregatorsList, windowType, dataWindows, aggregatedWindows):
    '''
    :param aggregatorsList: list of functions that reduce the data in a window to a single line
    :param windowType: one of 'short' , 'long', 'entire'
    :param dataWindows: list of (structured) arrays
    :param aggregatedWindows:  list of reduced windows, either short, if windowType is 'long', or long windows if windowType is 'entire'
    :return: a structured array: contains a line for every window in dataWindows.
    '''
    if windowType == 'short':
        header, firstAggregatedWindow = aggregate(aggregatorsList, windowType, dataWindows[0], None)
        table = [firstAggregatedWindow]
        for timeWindow in dataWindows[1:]:
            _, row = aggregate(aggregatorsList, windowType, timeWindow, None)
            table.append(row)
    elif windowType == 'long':
        assert len(dataWindows) == len(aggregatedWindows), "len(dataWindows), len(aggregatedWindows): {}, {}"\
                                                                       .format(len(dataWindows), len(aggregatedWindows))
        aggIter = iter(aggregatedWindows)
        header, firstAggregatedWindow = aggregate(aggregatorsList, windowType, dataWindows[0], aggIter.next())
        table = [firstAggregatedWindow]
        for timeWindow in dataWindows[1:]:
            item = aggIter.next()
            _, row = aggregate(aggregatorsList, windowType, timeWindow, item)
            table.append(row)
    else: #windowType == 'entire':
        header, row = aggregate(aggregatorsList, windowType, dataWindows, aggregatedWindows)
        table = [row]


    dt = zip(header, len(header)*['f4']) # TODO: set the field type in a constant. are 4 bytes enough?
    rows = [tuple(list(row[0])) for row in table]
    assert len(rows[0]) == len(dt), 'number of fields does not match number of values in row!'
    ret = np.array(rows, dtype=dt)
    return ret

def divideToWindows(dataMatrix, windowLength):
    '''
    :param dataMatrix:
    :param windowLength:
`    :return: windows is a list of arrays
    '''
    divided =  [dataMatrix[a:a+windowLength] for a in range(0, len(dataMatrix)-windowLength + 1, windowLength)]
    return  divided

def createFeatures(outputDir = UNIFIED_TABLES_FOLDER):
    #define the aggregators for each table
    aggregatorsListShort = [numSamplesInFreqRange]
    aggregatorsListLong = [statisticsForAllColoumns, numSubWindowsInFreqRange]
    aggregatorsListEntire = [statisticsForAllColoumns, averageOnWindows, waveletCompressForAllColoumns]

    #initialize
    dataMatrix = dict()
    labelsMatrix = dict()
    aggregatedSubWindows = dict()
    aggregatedWindows = dict()
    aggregatedLabels = []
    aggregatedPatientNames= []
    #create 5 sec per line table, per person
    for patient in PATIENTS: # TODO: change back to PATIENTS!
        #read patient data, separate between actual features and labels
        print "Generating features for ", patient
        patientData = readFileToFloat(os.path.join(outputDir, "DATAFILE_" + patient + ".csv"))
        names = np.array(patientData.dtype.names)
        labelField = names[np.where((names == 'Is_Sick'))]
        dataFields = names[np.where((names != 'Is_Sick'))]
        patientLabels = patientData[list(labelField)]
        patientData = patientData[list(dataFields)]

        # insert data into matrix
        labelsMatrix[patient] = patientLabels
        dataMatrix[patient] = patientData

        #divide to windows, and reduce/aggregate every window into a line.
        dataSubWindows = divideToWindows(patientData, SHORT_TIME_WINDOW) # dataSubWindows is a list of structured arrays.

        aggregatedSubWindows[patient] = createTimeWindowTable(aggregatorsListShort, 'short', dataSubWindows, None) #TODO check if easy to return the table
        logger.info("first aggr subWindow:\n{}".format(aggregatedSubWindows[patient].dtype.names))
        logger.info("{}".format(aggregatedSubWindows[patient][0]))

        #write to patient file
        shortAggregatedFile = open(os.path.join(outputDir, "SHORTFILE_" + patient + ".csv"), 'w')
        writer = csv.writer(shortAggregatedFile, lineterminator='\n')
        patientTable = aggregatedSubWindows[patient] # every line is the reduction of a 5 sec window of current patient's data
        writer.writerow(patientTable.dtype.names)
        writer.writerows(patientTable)

    logger.info("Wrote aggregatedSubWindows table to File")
    #create 5 min per line table
    assert len(PATIENTS) == len(dataMatrix), "len(PATIENTS)({}) != len(dataMatrix)({}) !: " \
        .format(len(PATIENTS), len(dataMatrix))
    for patient, patientData in dataMatrix.items():
        longAggregatedFile = open(os.path.join(outputDir, "LONGFILE_" + patient + ".csv"), 'w')
        dataWindows = divideToWindows(patientData, LONG_TIME_WINDOW)
        subWindows = divideToWindows(aggregatedSubWindows[patient], LONG_TIME_WINDOW/SHORT_TIME_WINDOW)

        aggregatedWindows[patient] = (createTimeWindowTable(aggregatorsListLong, 'long', dataWindows, subWindows))

        #create labels
        num_windows = len(aggregatedWindows[patient])
        is_sick = float(patient in SICK_PATIENTS)
        aggregatedLabels.extend(num_windows * [is_sick])

        #create list of names
        aggregatedPatientNames.extend(num_windows * [patient])

        writer = csv.writer(longAggregatedFile, lineterminator='\n')
        patientTable = aggregatedWindows[patient] # every line is the reduction of a 5 min window of current patient's data
        writer.writerow(patientTable.dtype.names)
        writer.writerows(patientTable)
        logger.info("Wrote aggregatedWindows table to File, patient: {}".format(patient))

    with open(UNIFIED_AGGREGATED_DATA_PATH, 'w') as unified_entire_file:
        listOfPData = [aggregatedWindows[patient] for patient in PATIENTS]
        unified_aggregated_table = nprf.stack_arrays(tuple(listOfPData), usemask=False)
        writer = csv.writer(unified_entire_file, lineterminator='\n')
        writer.writerow(unified_aggregated_table.dtype.names)
        writer.writerows(unified_aggregated_table)

    with open(UNIFIED_AGGREGATED_LABELS_PATH, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(aggregatedLabels)

    with open(UNIFIED_AGGREGATED_PATIENT_NAMES_PATH, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(aggregatedPatientNames)

    #create patient per line table
    aggregatedEntires = dict()
    for patient, patientData in dataMatrix.items():
        entireAggregatedFile = open(os.path.join(outputDir, "ENTIREFILE_" + patient + ".csv"), 'w')
        aggregatedEntires[patient] = createTimeWindowTable(aggregatorsListEntire, 'entire', patientData, aggregatedWindows[patient])
        writer = csv.writer(entireAggregatedFile, lineterminator='\n')
        writer.writerow(aggregatedEntires[patient].dtype.names)
        writer.writerows(aggregatedEntires[patient])

    with open(UNIFIED_ENTIRE_DATA_PATH, 'w') as unified_entire_file:
        listOfPData = [aggregatedEntires[patient] for patient in PATIENTS_test]
    with open(UNIFIED_ENTIRE_DATA_PATH, 'w') as unified_entire_file:
        listOfPData = [aggregatedEntires[patient] for patient in PATIENTS]
        unified_entire_table =nprf.stack_arrays(tuple(listOfPData), usemask=False)
        writer = csv.writer(unified_entire_file, lineterminator='\n')
        writer.writerow(unified_entire_table.dtype.names)
        writer.writerows(unified_entire_table)

    # write labels to files
    with open(UNIFIED_ENTIRE_LABELS_PATH, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        entireLabels = [float((patient in SICK_PATIENTS)) for patient in dataMatrix.keys()]
        # patientList = dataMatrix.keys()
        # writer.writerow(patientList)
        writer.writerow(entireLabels)


if __name__ == "__main__":
    createFeatures()