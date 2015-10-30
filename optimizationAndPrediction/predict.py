__author__ = 'Inspiron'

from random import shuffle

from utils.constants import *
from utils.utils import *
from optimize import optimizeHyperParams
import sklearn.svm #TODO other learners as well
import sklearn.ensemble
import sklearn.linear_model
from FeatureSelection import SelectFeatures
from sklearn.cross_validation import LeavePLabelOut
from sklearn import grid_search
import dumper
import csv
import pdb

'''
for all patients,
line per entire data - predict by each feature of the line, all the features, and features of transform
average of all lines per 5 min of patient - get one line per patient - should be just another features in the 'line per patient'
lines per 5 min of data - predict by each feature, all the features.
'''

def lossFunction(estimator, X, y, names=None):
    pdb.set_trace()
    loss = 0.0
    for data,label in zip(X,y):
        #print "lossFunction: ",estimator
        #print "lossFunction: ", data
        #print "lossFunction: ", labels
        #print "lossFunction: ",estimator.predict(data)[0][0]
        #weird patch, suddenly getting weired arrays for data and label... 30.10.15, 08:15, jonathan
        if estimator.predict(data)[0] != label:
            loss += 1
    loss = loss / len(X)
    return 1-loss

def twoStepsLoss(estimator, X, y, names):
    print names
    folds = LeavePLabelOut(names, p=1) #ugly patch - correct syntax?
    folds = [tup for tup in folds]
    loss = 0.0
    for testIndices in folds[:2]:
        print "in fold"
        testData = X[testIndices]
        testLabels = y[testIndices]
        testLabel = (y[testIndices])[0]
        sickCount = 0.0
        for data in testData:
            sickCount = sickCount + (estimator.predict(data)[0])
        sickCount = sickCount / len(X)
        if sickCount > 0.5: #mostly sick
            if testLabel == 0:
                loss = loss + 1
        else:
            if testLabel == 1:
                loss = loss + 1
    loss = 1 - (loss/2)
    return loss


def predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, isEntire):
    listOfLossValuesPerFeature = dict()
    features = linePerPatientData.dtype.names

    for feature in features:
        values = linePerPatientData[feature]
        dataForClassifier = [[v] for v in values]
        result = crossValidate(predictor, dataForClassifier, linePerPatientLabels, lossFunction, NUMBER_OF_FOLDS)
        error = np.mean(result)
        listOfLossValuesPerFeature[feature] = error
    data = castStructuredArrayToRegular(linePerPatientData)
    result = crossValidate(predictor, data, linePerPatientLabels, lossFunction, NUMBER_OF_FOLDS)
    error = np.mean(result)
    listOfLossValuesPerFeature ['all'] = error

    if isEntire:
        print "isEntire True!"
        r = re.compile(r'(.*_DCT_coeff_).*')
        transformFeatures = filter_fields_by_name(linePerPatientData.dtype.names, r)
        assert len(transformFeatures) > 1, "no transform features!"
        data = castStructuredArrayToRegular(linePerPatientData[transformFeatures])
        result = crossValidate(predictor, data, linePerPatientLabels, lossFunction, NUMBER_OF_FOLDS)
        error = np.mean(result)
        listOfLossValuesPerFeature['transform_features'] = error
        print listOfLossValuesPerFeature['transform_features']

    return listOfLossValuesPerFeature


def  plot(errorFeatureTupleDict, resultPath):
    sortedErrors = sorted(errorFeatureTupleDict.items(), key= lambda tup: tup[1])
    # sorted(errorFeatureTupleList, lambda x: x[1])
    res = [list(t) for t in sortedErrors]
    print res
    with open(resultPath, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(res)
    return

def create_cross_validation_idxs(num_samples, num_folds):
    '''Creates num_folds different and foreign folds of the data.
    This method returns a collection of (training_samples_idxs, validation_samples_idxs) pairs,
    every pair must have a single, different fold as the validation set, and the other folds as training.
    PICK THE ELEMENTS OF EACH FOLD RANDOMLY. The collection needs to have num_folds such pairs.'''
    sample_set = set(range(num_samples))
    fold_size = int(num_samples/num_folds)

    # Shuffle the samples, each fold_size consecutive indexes in the shuffle result will be some Sk
    shuffled_samples = list(sample_set)
    shuffle(shuffled_samples)

    # Calculate all training-validation pairs
    pairs = []
    for fold_start in range(0,num_samples,fold_size):
        validation = set(shuffled_samples[fold_start:fold_start+fold_size])
        training = sample_set - validation
        pairs.append((list(training),list(validation)))
    return pairs

def crossValidate(predictor, data, labels, lossFunction, numFolds):
    folds = create_cross_validation_idxs(len(data), numFolds)
    errors = []
    for trainIndices, testIndices in folds:
        trainData = [data[i] for i in trainIndices]
        trainlabels = [labels[i] for i in trainIndices]
        testData = [data[i] for i in testIndices]
        testLabels = [labels[i] for i in testIndices]
        if np.all(trainlabels == trainlabels[0]): #can't train on elements that are all from the same group
            continue
        predictor.fit(trainData, trainlabels)
        errors.append(lossFunction(predictor, testData , testLabels))
    return errors

def predictOnEntire():
    # learning on "Entire"
    #==============================================================================================
    linePerPatientData = readFileToFloat(UNIFIED_ENTIRE_DATA_PATH)
    linePerPatientLabels = readFileToFloat(UNIFIED_ENTIRE_LABELS_PATH, names = None)


    #each result is a ***Dictionary*** with all learning Iterations (features, 'all', transformation')
    #==============================================================================================

    predictor = sklearn.svm.SVC()
    svmLinePerPatientResults  = predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, True)
    print "svm on entire is done!"

    predictor = sklearn.linear_model.LogisticRegression('l2', True)
    logisticRegLinePerPatientResults = predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, True)
    print "logisticReg on entire is done!"


    predictor = sklearn.ensemble.RandomForestClassifier(4) #4 is sqrt of number of patients
    randomForestLinePerPatientResults = predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, True)
    print "randomForest on entire is done!"


    print "plotting..."
    plot(svmLinePerPatientResults, SVM_RES_ENTIRE_PATH)
    plot(logisticRegLinePerPatientResults, LOGISTIC_RES_ENTIRE_PATH)
    plot(randomForestLinePerPatientResults, FOREST_RES_ENTIRE_PATH)

def tuneAndTrain(predictorType, data, labels, patientIds, numFolds, lossFunction = lossFunction):
    '''
    :param data: data matrix, a structured array.
    :param predictorType: one of: {'SVM', 'RF'}
    :param patientIds: May be ints, strings, etc. denoting which patient every line is taken from.
    :return: the mean error of an optimized predictor of type predictorType, and the optimized, trained predictor.
    '''
    
    # pdb.set_trace()
   
    patientIds = np.array(patientIds[0])
    folds = LeavePLabelOut(patientIds, p=2) #
    folds = [tup for tup in folds]
    errors = []

    for trainIndices, testIndices in folds[:numFolds]:
        #Tuning
        #get actual data and labels for current fold
        trainData = data[trainIndices]
        trainLabels = labels[trainIndices]
        testData = data[testIndices]
        testLabels = labels[testIndices]
        testNames = patientIds[testIndices]
        if np.all(trainLabels == trainLabels[0]):
            continue #can't train on elements that are all from the same group

        # todo: for testing - skip feature selection
        # selectedFeatures = SelectFeatures(trainData, trainLabels)
        # selectedTrainData = [trainData[f] for f in selectedFeatures]
        # selectedTestData = [testData[f] for f in selectedFeatures]
        selectedTrainData = trainData
        selectedTestData = testData

        # to get the data in a list-of-list format that optimizeHyperParams expects.
        selectedTrainData = [list(tup) for tup in selectedTrainData]
        selectedTestData = [list(tup) for tup in selectedTestData]

        predictor = optimizeHyperParams(selectedTrainData, trainLabels, predictorType)

        #Training
        #predictor.fit(selectedFeaturesTrainData, trainLabels) //optimizeHyperParams also trains

        #Testing
        errors.append(lossFunction(predictor, selectedTestData, testLabels, testNames))

    return np.array(errors).mean()

def predictOnWindows(data, lables, names):
    # learning on data divided into time windows
    #==============================================================================================


    #==============================================================================================
    #each result is a Dictionary with all learning Iterations (features, 'all')
    #==============================================================================================
    predictor_types = ['SVM', 'RF'] #TODO: add the rest
    
    results = {}
    #predictors = dict()
    #predictors['SVM'] = sklearn.svm.SVC()
    #predictors['randomForest'] = sklearn.ensemble.RandomForestClassifier() #65 is aprox the sqrt of the fiveMinutes we have in FIRSTDATA
   # predictors['logisticRegL2'] = sklearn.linear_model.LogisticRegression('l2', dual = False, multi_class='ovr')
   # predictors['logisticRegL1'] = sklearn.linear_model.LogisticRegression('l1', multi_class='ovr')

    # regular prediction
    for predictor in predictor_types:
        results[predictor] = tuneAndTrain(predictor, data, lables, names, NUMBER_OF_FOLDS)
        print "{} on windows is done!".format(predictor)


    #This is 2 steps prediction - commitee - not parallel to regular prediction above
    #for predictor in predictors.keys():
    #    results[predictor] = tuneAndTrain(predictors[predictor], data, lables, names, NUMBER_OF_FOLDS, twoStepsLoss)
    #    print "{} on windows is done!".format(predictor)

    # print "writing results to file..."
    # paths = [SVM_RES_WINDOWS_PATH,LOGISTIC_RES_WINDOWS_PATH,FOREST_RES_WINDOWS_PATH]
    # for res, path in zip(results.values(), paths):

    for type, res in results.items():
        print "error on {} is: {}".format(type, res)
    return results

def predictOnFeatures(data, labels):
    results = {}
    predictors = dict()
    predictors['SVM'] = sklearn.svm.SVC()
    predictors['randomForest'] = sklearn.ensemble.RandomForestClassifier(max_features="sqrt") #65 is aprox the sqrt of the fiveMinutes we have in FIRSTDATA
    # predictors['logisticRegL2'] = sklearn.linear_model.LogisticRegression('l2', dual = False, multi_class='ovr')
    # predictors['logisticRegL1'] = sklearn.linear_model.LogisticRegression('l1', multi_class='ovr')

    #regular prediction
    for predictor in predictors.keys():
        results[predictor] = predictByFeatures(predictors[predictor], data, labels, isEntire=False)
        print "{} on features is done!".format(predictor)
    return results



def predict():
    try:
        os.mkdir(RESULTS_FOLDER)
    except OSError:
        pass

    # predicting on data divided into windows:
    #-----------------------------------------
    #linePerFiveMinutesData = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
    #linePerFiveMinutesLabels = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)
    #linePerFiveMinutesNames = readFileAsIs(UNIFIED_AGGREGATED_PATIENT_NAMES_PATH)
    #results = predictOnWindows(linePerFiveMinutesData, linePerFiveMinutesLabels, linePerFiveMinutesNames)

    # predicting on line-per-sample data:
    #-----------------------------------------
    data = readFileToFloat(DATA_TABLE_FILE_PATH)
    labels = readFileToFloat(LABELS_FOR_DATA_TABLE_FILE_PATH , names = None)
    results = predictOnFeatures(data, labels)


    
    # writing results to file
    #-----------------------------------------
    with open(UNIFIED_RESULTS_PATH,'w') as theFile:
        writer = csv.writer(theFile)
        t = results.keys()[0]
        keys = results[t].keys()
        writer.writerow(["Feature"]+results.keys())
        for key in keys:
            row = [key] + [d[key] for d in results.values()]
            writer.writerow(row)
    #plotData(linePerPatientData, labelsPerPatients)


if __name__=='__main__':
    predict()
