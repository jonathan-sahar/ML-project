__author__ = 'Inspiron'

import numpy as np
from constants import *
import sklearn
import csv
import matplotlib.pyplot as plt
import itertools
import re
'''

def readData():
    filePath = 'C:\ML\parkinson\orEstimation\SVM_IMPUT.csv'
    newFile = open(filePath, 'r')
    reader = csv.reader(newFile)
    allLines = []
    for row in reader:
        line = []
        for item in row:
            line.append(float(item))
        #line = [float(value) for value in row if not match.search(value)]
        #print("line (floats): {}".format(line))
        allLines.append(line)
    #print allLines
    return allLines

def predByOneFeature(X):
    error = 0
    counter = 0
    for i,j in itertools.product(range(0,16), repeat=2):
        if i >= j:
            continue
        counter += 1
        trainList = list(X)
        testlist = [trainList.pop(max(i,j))]
        testlist.append(trainList.pop(min(i,j)))
        #print testlist
        trainLabel = list(Y)
        testLabel = [trainLabel.pop(max(i,j))]
        testLabel.append(trainLabel.pop(min(i,j)))
        clf = svm.SVC(kernel='linear', C=1)
        #print trainList
        #print trainLabel
        clf.fit(trainList, trainLabel)
        results = clf.predict(testlist)
        print results
        for index in range(0,2):
            if results[index] != testLabel[index]:
                error += 1
                #print error
    return float(error)/float(counter*2)

def predictByOneFeature(X):
    tmpList = list(X)
    X = []
    for item in tmpList:
        X.append([item])
    #print X
    error = pred(X)
    return error


for all patients,
line per entire data - predict by each feature of the line, all the features, and features of transform
average of all lines per 5 min of patient - get one line per patient - should be just another features in the 'line per patient'
lines per 5 min of data - predict by each feature, all the features.


def getTransformationFeatures():
    return

def svmPredictLinePerPatient(linePerPatientData,LabelsPerPatients):
    results = []
    predictor = sklearn.svm.SVC(kernel='linear', C=1)
    for k in range(0, NUMBER_OF_ENTIRE_FEATURES):
        linePerPatientMatrix = np.array(linePerPatientData)
        data = list(linePerPatientMatrix[:,feature])
        feature = features[k]
        #result = cross_validate(svm, featurePerPatientData, LabelsPerPatients)
        result = sklearn.cross_validation.cross_val_score(predictor, data, LabelsPerPatients, NUMBER_OF_FOLDS)
        np.
        results.append((result, feature))

    data = linePerPatientData
    result = sklearn.cross_validation.cross_val_score(sklearn.svm, data, LabelsPerPatients)
    results.append((result, 'all'))

    data = getTransformationFeatures()
    result = sklearn.cross_validation.cross_val_score(sklearn.svm, data, LabelsPerPatients)
    results.append((result, 'transformation'))

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



    #print data
    dataArray = np.array(data)
    #print data
    features = ['diffSecs','N.samples','x.mean','x.absolute.deviation','x.standard.deviation','x.max.deviation','x.PSD.1','x.PSD.3','x.PSD.6','x.PSD.10','y.mean','y.absolute.deviation','y.standard.deviation','y.max.deviation','y.PSD.1','y.PSD.3','y.PSD.6','y.PSD.10','z.mean','z.absolute.deviation','z.standard.deviation','z.max.deviation','z.PSD.1','z.PSD.3','z.PSD.6','z.PSD.10','diffSecs','absolute.deviation','standard.deviation','max.deviation','MFCC.1','MFCC.2','MFCC.3','MFCC.4','MFCC.5','MFCC.6','MFCC.7','MFCC.8','MFCC.9','MFCC.10','MFCC.11','MFCC.12']
    error_est = []

    for k in range(0,NUMBER_OF_FEATURES):
        X = dataArray[:,k]
        feature = features[k]
        error = predictByOneFeature(X)
        error_est.append((feature,error))

    error = 0
    counter = 0
    X = data[0:27]
    #for pair in itertools.product(X, repeat=2):
    for i,j in itertools.product(range(0,16), repeat=2):
        #print "hi"
        if i >= j:
            continue
        counter += 1
        trainList = list(X)
        testlist = [trainList.pop(max(i,j))]
        testlist.append(trainList.pop(min(i,j)))
        #print testlist
        trainLabel = list(Y)
        testLabel = [trainLabel.pop(max(i,j))]
        testLabel.append(trainLabel.pop(min(i,j)))
        clf = svm.SVC(kernel='linear', C=1)
        clf.fit(trainList, trainLabel)
        results = clf.predict(testlist)
        for i in range(0,2):
            if results[i] != testLabel[i]:
                error += 1
    error_est.append(('All',float(error)/float(counter*2)))
    a = sorted(error_est, key=lambda x:x[1])
    for e in  error_est:
        print e
'''
    for k in range(27,42):
        print k
        X = data[:,k]
        tmpList = list(X)
        X = []
        for item in tmpList:
            X.append([item])
        #print X
        feature = features[k]
        error = pred(X)
        error_est.append((feature,error))
'''




    #X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, X, test_size=0.125, random_state=0)
    #scores = cross_validation.cross_val_score(clf, X.data, X.target, cv=5)

    #print scores








    ((data_train, label_train), (data_test, label_test)) = load_data()

    num_of_lambdas = 10
    lambda_vals = linspace(0.1,1000,num_of_lambdas)
    errs = zeros([num_of_lambdas,10,2])
    i = 0
    folds = create_cross_validation_idxs(size(label_train), 8)
   ''' # print("len of folds is {}\nvalue of i is {}".format(len(folds), i))
    #for (train_indices, vld_indices) in folds:
        #for ind,lambda_val in enumerate(lambda_vals):
     # '''      # print("ind is {}\n".format(ind))
            #sub-divide to training and validation sets:
     '''       data_vld, label_vld = data_train[vld_indices, :],label_train[vld_indices]
            data_train_fold, label_train_fold = data_train[train_indices, :], label_train[train_indices]

            #Solve kernelized ridge regression:
            gram_matrix = polynomial(data_train_fold, data_train_fold, 3)
            m = len(label_train_fold)
            inversed_temp_matrix = inv(2.0/m * dot(gram_matrix, gram_matrix) + lambda_val *gram_matrix)
            alpha_opt = 2.0/m * dot(label_train_fold, dot(gram_matrix, inversed_temp_matrix))

            y_train = dot(alpha_opt,gram_matrix) #prediction on train_fold
            errs[ind, i, 1] = mean(power(y_train-label_train_fold,2))

            y_regress = dot(alpha_opt,polynomial(data_train_fold,data_vld, 3)) #prediction on validation for this fold
            errs[ind, i, 0] = mean(power(y_regress-label_vld,2))
        # print(" changing value of i from {} to {}".format(i, i+1))
        i = i+1
    best_lambda_idx = argmin(mean(errs[:,:,0], axis=1))
    best_lambda = lambda_vals[best_lambda_idx]

    #Plot training and validation errors as a function of lambda, as well as the final test error for best_lambda
    gram_matrix = polynomial(data_train, data_train, 3)
    m = len(label_train)
    inversed_temp_matrix = inv(2.0/m * dot(gram_matrix, gram_matrix) + best_lambda*gram_matrix)
    alpha_opt_for_test = 2.0/m * dot(label_train, dot(gram_matrix, inversed_temp_matrix))

    y_test = dot(alpha_opt_for_test,polynomial(data_train,data_test,3))
    test_error = mean(power(y_test-label_test,2))
    x_axis_for_test_error = tile(test_error,size(lambda_vals))

    validation_errs = mean(errs[:,:,0], axis=1)
    train_errs = mean(errs[:,:,1], axis=1)

    fig = plt.figure()
    fig.suptitle('Error on Train and Test Data vs Lambda', fontsize=14, fontweight='bold')
    graph = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    graph.set_xlabel('Lambda')
    graph.set_ylabel('Error')

    graph.plot(lambda_vals,train_errs,'r',lambda_vals,validation_errs,'b')
    graph.plot(lambda_vals,x_axis_for_test_error,'g')

    graph.grid()
    plt.show()

    '''


'''
SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0, degree=3,
gamma=0.0, kernel='rbf', max_iter=-1, probability=False, random_state=None,
shrinking=True, tol=0.001, verbose=False)
'''

'''