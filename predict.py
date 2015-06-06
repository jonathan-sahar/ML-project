__author__ = 'Inspiron'

import numpy as np
from constants import *
import sklearn
import csv
import matplotlib.pyplot as plt
import itertools
import re


'''
for all patients,
line per entire data - predict by each feature of the line, all the features, and features of transform
average of all lines per 5 min of patient - get one line per patient - should be just another features in the 'line per patient'
lines per 5 min of data - predict by each feature, all the features.
'''

def getTransformationFeatures():
    return


def svmPredictLinePerPatient(linePerPatientData,LabelsPerPatients):
    predictor = sklearn.svm.SVC(kernel='linear')
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, True)
    return results


def logisticRegPredictLinePerPatient(linePerPatientData,LabelsPerPatients):
    predictor = sklearn.linear_model.LogisticRegression('l2', True)
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, True)
    return results


def randomForestPredictLinePerPatient(linePerPatientData,LabelsPerPatients):
    predictor = sklearn.ensemble.RandomForestClassifier(4) #4 is sqrt of number of patients
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, True)
    return results

def svmPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor = sklearn.svm.SVC(kernel='linear')
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False) #TODO maybe better creating lose function
    return results

def logisticRegPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor = sklearn.linear_model.LogisticRegression('l2', False)
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False)
    return results

def randomForestPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor = sklearn.ensemble.RandomForestClassifier(65) #65 is aprox the sqrt of the fiveMinutes we have in FIRSTDATA
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False)
    return results

def lossFunction(estimator, X, y):
    loss = 0.0
    for a,b in X,y:
        if estimator.predict(a) != b:
            loss += 1
    loss = loss / len(X)
    return loss

def predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, isEntire):
    results = []
    for k in range(0, NUMBER_OF_ENTIRE_FEATURES):
        linePerPatientMatrix = np.array(linePerPatientData)
        data = list(linePerPatientMatrix[:,feature])
        feature = entireFeatures[data.pop()] #the first item is the feature name
        #cross_validate
        result = sklearn.cross_validation.cross_val_score(predictor, data, LabelsPerPatients,  lossFunction, NUMBER_OF_FOLDS)
        error = np.mean(result)
        results.append((error, feature))

    data = linePerPatientData
    result = sklearn.cross_validation.cross_val_score(sklearn.svm, data, LabelsPerPatients)
    error = np.mean(result)
    results.append((error, 'all'))

    if isEntire:
        data = getTransformationFeatures()
        result = sklearn.cross_validation.cross_val_score(sklearn.svm, data, LabelsPerPatients)
        error = np.mean(result)
        results.append((error, 'transformation'))

    return results

def readFileToFloat(filePath): #TODO same code in another module. open util module
    '''
    Assumes file  contains headers
    :param filePath:
    :return:
    '''
    newFile = open(filePath, 'r')
    data = np.genfromtxt(filePath, dtype=float, delimiter=',', names = True, case_sensitive=True)
    field_names = np.array(data.dtype.names)
    r = re.compile(r'(.*time.*|.*patient.*)',re.IGNORECASE)
    vmatch = np.vectorize(lambda x:bool(r.match(x)))
    mask = ~vmatch(field_names) # mask is true where field name doesn't contain 'time' or 'patient'
    return data[field_names[mask]]

def readFileAsIs(filePath):  #TODO same code in another module. open util module
    newFile = open(filePath, 'r')
    reader = csv.reader(newFile)
    allLines = [row for row in reader]
    newFile.close()
    return allLines

def plot(errorFeatureTupleList):
    sorted(errorFeatureTupleList, lambda x: x[1])
    print errorFeatureTupleList
    return

if __name__=='__main__':
    linePerPatientData = readFileToFloat(UNIFIED_ENTIRE_PATH)
    LabelsPerPatients = readFileAsIs(UNIFIED_ENTIRE_LABELS_PATH) #[0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1] #by the order in constants.py

    #each result is a Dictionary with all learning Iterations (features, 'all', transformation')
    svmLinePerPatientResults = svmPredictLinePerPatient(linePerPatientData,LabelsPerPatients)
    logisticRegLinePerPatientResults = logisticRegPredictLinePerPatient(linePerPatientData,LabelsPerPatients)
    randomForestLinePerPatientResults = randomForestPredictLinePerPatient(linePerPatientData,LabelsPerPatients)

    linePerFiveMinutesData = readFileToFloat(UNIFIED_AGGREGATED_PATH)
    LabelsPerLines = readFileAsIs(UNIFIED_AGGREGATED_LABELS_PATH)

    #each result is a Dictionary with all learning Iterations (features, 'all')
    svmLinePerFiveMinutesResults = svmPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    logisticRegLinePerFiveMinutesResults = logisticRegPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    randomForestLinePerFiveMinutesResults = randomForestPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)

    plot(svmLinePerPatientResults)
    plot(logisticRegLinePerPatientResults)
    plot(randomForestLinePerPatientResults)
    plot(svmLinePerFiveMinutesResults)
    plot(logisticRegLinePerFiveMinutesResults)
    plot(randomForestLinePerFiveMinutesResults)

