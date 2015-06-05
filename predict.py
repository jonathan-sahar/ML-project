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
    predictor = sklearn.linear_model.LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0,\
    fit_intercept=True, intercept_scaling=1, class_weight=None, random_state=None, solver='liblinear',\
    max_iter=100, multi_class='ovr', verbose=0)
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, True)
    return results


def randomForestPredictLinePerPatient(linePerPatientData,LabelsPerPatients):
    predictor =sklearn.ensemble.RandomForestClassifier(n_estimators=10, criterion='gini', max_depth=None, min_samples_split=2, \
    min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, \
    bootstrap=True, oob_score=False, n_jobs=1, random_state=None, verbose=0, warm_start=False, class_weight=None)
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, True)
    return results

def  svmPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor = sklearn.svm.SVC(kernel='linear')
    results = predictByFeatures(predictor, linePerPatientData, LabelsPerPatients, False)
    return results

def logisticRegPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines):
    predictor =
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
        #result = cross_validate(svm, featurePerPatientData, LabelsPerPatients)
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

