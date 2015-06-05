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
    predictor =sklearn.ensemble.RandomForestClassifier(4) #4 is sqrt of number of patients
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, True)
    return results

def  svmPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor = sklearn.svm.SVC(kernel='linear')
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False) #TODO maybe better creating lose function
    return results

def logisticRegPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor = sklearn.linear_model.LogisticRegression('l2', False)
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False)
    return results

def randomForestPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor =
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False)
    return results

def predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, isEntire):
    results = []
    for k in range(0, NUMBER_OF_ENTIRE_FEATURES):
        linePerPatientMatrix = np.array(linePerPatientData)
        data = list(linePerPatientMatrix[:,feature])
        feature = entireFeatures[data.pop()] #the first item is the feature name
        #cross_validate
        result = sklearn.cross_validation.cross_val_score(predictor, data, LabelsPerPatients, NUMBER_OF_FOLDS)
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


if __name__=='__main__':
    linePerPatientData = readLinePerPatientData()
    LabelsPerPatients = [0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1] #by the order in constants.py

    #each result is a Dictionary with all learning Iterations (features, 'all', transformation')
    svmLinePerPatientResults = svmPredictLinePerPatient(linePerPatientData,LabelsPerPatients)
    logisticRegLinePerPatientResults = logisticRegPredictLinePerPatient(linePerPatientData,LabelsPerPatients)
    randomForestLinePerPatientResults = randomForestPredictLinePerPatient(linePerPatientData,LabelsPerPatients)

    linePerFiveMinutesData = readLinePerFiveMinutesData()
    LabelsPerLines = getLabelsPerLine()#(np.array(linePerFiveMinutesData))(:LABEL_COLUMN) need to do real extraction

    #each result is a Dictionary with all learning Iterations (features, 'all')
    svmLinePerFiveMinutesResults = svmPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    logisticRegLinePerFiveMinutesResults = logisticRegPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    randomForestLinePerFiveMinutesResults = randomForestPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)

    plot()

