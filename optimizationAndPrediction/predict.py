from random import shuffle

from utils.constants import *
from utils.utils import *
from optimize import optimizeHyperParams
from sklearn.svm import SVC  # TODO other learners as well
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from FeatureSelection import SelectFeatures
from sklearn.cross_validation import LeavePLabelOut
from sklearn import grid_search

import csv
import pdb

import warnings
warnings.filterwarnings("ignore")
'''
for all patients:
line per entire data - predict by each feature of the line, all the features,
and features of transform average of all lines per 5 min of patient
- get one line per patient - should be just another features in the
'line per patient' lines per 5 min of data - predict by each feature,
all the features.
'''


def lossFunction(estimator, X, y, names=None):
    # pdb.set_trace()
    loss = 0.0
    for data, label in zip(X, y):
        if estimator.predict(data)[0] != label:
            loss += 1
    loss = loss / len(X)
    return 1-loss

def twoStepsLoss(estimator, X, y, names):
    folds = LeavePLabelOut(names, p=1) #ugly patch - correct syntax?
    folds = [tup for tup in folds]
    loss = 0.0
    for otherPatient ,testIndices in folds[:2]:
        testIndices = np.array(testIndices)
        testData = [X[index] for index in testIndices]
        #testData = testData[0]
        testLabels = [y[index] for index in testIndices]
        testLabel = (y[testIndices[0]])
        sickCount = 0.0
        for data in testData:
            sickCount = sickCount + estimator.predict(data)
        sickCount = sickCount / len(testLabels)
        if sickCount > 0.5: #mostly sick
            if testLabel == 0:
                loss = loss + 1
        else:
            if testLabel == 1:
                loss = loss + 1
    success = 1 - (loss/2)
    return success


def predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, isEntire):
    listOfLossValuesPerFeature = dict()
    features = linePerPatientData.dtype.names
    print "entering features loop"
    for feature in features:
        values = linePerPatientData[feature]
        print "[predictByFeatures] predicting on feature: {}".format(feature)
        dataForClassifier = [[v] for v in values]
        result = crossValidate(predictor, dataForClassifier, linePerPatientLabels, lossFunction, NUMBER_OF_FOLDS)
        error = np.mean(result)
        listOfLossValuesPerFeature[feature] = error
    print "[predictByFeatures] finished prediction on feature: {}".format(feature)
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
    count = 0 #for debug only
    folds = create_cross_validation_idxs(len(data), numFolds)
    errors = []
    print "[crossValidate] entering main loop"
    for trainIndices, testIndices in folds:
        count = count + 1 #for debug only
        print "[crossValidate] starting fold No. {}".format(count)
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

    predictor = SVC()
    svmLinePerPatientResults  = predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, True)
    print "svm on entire is done!"

    predictor = LogisticRegression('l2', True)
    logisticRegLinePerPatientResults = predictByFeatures(predictor, linePerPatientData, linePerPatientLabels, True)
    print "logisticReg on entire is done!"


    predictor =RandomForestClassifier(4) #4 is sqrt of number of patients
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
    chosen_folds = np.random.randint(len(folds), size = numFolds)
    folds = [tup for tup in folds] # make a proper list out o fthe iterator object returned by LeavePLabelOut
    folds = [folds[i] for i in chosen_folds] # slice out only a random sample of size numFolds
    errors = []
    fold_no = 0
    for trainIndices, testIndices in folds:
        fold_no += 1
        print "[tuneAndTrain] started fold no. {} out of total {}".format(fold_no, numFolds)
        #Tuning
        #get actual data and labels for current fold
        trainData = data[trainIndices]
        trainLabels = labels[trainIndices]
        testData = data[testIndices]
        testLabels = labels[testIndices]
        testNames = patientIds[testIndices]
        if np.all(trainLabels == trainLabels[0]):
            continue #can't train on elements that are all from the same group

        print "[tuneAndTrain] running feature selection..."
        # selectedFeatures = SelectFeatures(trainData, trainLabels)
        # pdb.set_trace()
        # selectedTestData = tuple([testData[f] for f in selectedFeatures])
        # selectedTrainData = tuple([trainData[f] for f in selectedFeatures])


        selectedTrainData = castStructuredArrayToRegular(trainData).tolist()
        selectedTestData = castStructuredArrayToRegular(testData).tolist()

        
        print "[tuneAndTrain] running optimizeHyperParams..."
        predictor = optimizeHyperParams(selectedTrainData, trainLabels, predictorType)

        #Training
        #predictor.fit(selectedFeaturesTrainData, trainLabels) //optimizeHyperParams also trains

        #Testing
        print "[tuneAndTrain] testing predictor..."
        errors.append(twoStepsLoss(predictor, selectedTestData, testLabels, testNames)) # change lossFunction to twoStepsLoss for conf_8

    return np.array(errors).mean()

def predictOnWindows(data, lables, names):
    # learning on data divided into time windows
    #==============================================================================================


    #==============================================================================================
    #each result is a Dictionary with all learning Iterations (features, 'all')
    #==============================================================================================
    # predictor_types = ['SVM', 'RF', 'logisticReg'] 
    predictor_types = ['RF']
    
    results = {}
    #predictors = dict()
    #predictors['SVM'] = SVC()
    #predictors['randomForest'] = RandomForestClassifier() #65 is aprox the sqrt of the fiveMinutes we have in FIRSTDATA
    # predictors['logisticRegL2'] = LogisticRegression('l2', dual = False, multi_class='ovr')
    # predictors['logisticRegL1'] = LogisticRegression('l1', multi_class='ovr')

    # regular prediction
    for predictor in predictor_types:
        print "running {} on windows".format(predictor)
        results[predictor] = tuneAndTrain(predictor, data, lables, names, NUMBER_OF_FOLDS)
        print "{} on windows is done!".format(predictor)


   # committee prediction
    for predictor in predictor_types:
        print "running {} on windows".format(predictor)
        results[predictor] = tuneAndTrain(predictor, data, lables, names, NUMBER_OF_FOLDS, twoStepsLoss)
        print "{} on windows is done!".format(predictor)

    for type, res in results.items():
        print "error on {} is: {}".format(type, res)
    return results

def predictOnFeatures(data, labels):
    results = {}
    predictors = dict()
    # predictors['SVM'] = SVC()
    predictors['randomForest'] = RandomForestClassifier(max_features="sqrt") #65 is aprox the sqrt of the fiveMinutes we have in FIRSTDATA
    # predictors['logisticReg'] = LogisticRegressionCV(Cs=10)
    # predictors['logisticRegL2'] = LogisticRegression('l2', dual = False, multi_class='ovr')
    # predictors['logisticRegL1'] = LogisticRegression('l1', multi_class='ovr')
    print "created predictor"
    #regular prediction
    for predictor in predictors.keys():
	print "predictByFeatures"
        results[predictor] = predictByFeatures(predictors[predictor], data, labels, isEntire=False)
        print "{} on features is done!".format(predictor)
    return results



def predict():
    try:
        os.mkdir(RESULTS_FOLDER)
    except OSError:
        pass
    try:
        os.mkdir("timing")
    except OSError:
        pass

    os.system('touch timing/start_time')
    print("predicting on data from {}".format(ROOT_DATA_FOLDER))    
    # predicting on data divided into windows:
    #-----------------------------------------
    # linePerFiveMinutesData = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
    # linePerFiveMinutesLabels = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)
    # linePerFiveMinutesNames = readFileAsIs(UNIFIED_AGGREGATED_PATIENT_NAMES_PATH)
    # data = linePerFiveMinutesData
    # labels = linePerFiveMinutesLabels 
    # names = linePerFiveMinutesNames 
    
    data, labels, names = getRandomSample(0.5)
    names = [names] # ugly hack: tuneAndTrain (called from predictOnWindows
                    # expects names to be the [0] element of another list)
    
    results = predictOnWindows(data, labels, names)
    # predicting on line-per-sample data:
    #-----------------------------------------
    # data = readFileToFloat(DATA_TABLE_FILE_PATH)
    # labels = readFileToFloat(LABELS_FOR_DATA_TABLE_FILE_PATH , names = None)
    # print "predicting on features invoke"
    # results = predictOnFeatures(data, labels)

    # print "writing results to file"
    
    # writing results to file
    #-----------------------------------------

    # Uncomment below for configuration No.1
    # with open(UNIFIED_RESULTS_PATH,'w') as theFile:
    #     writer = csv.writer(theFile)
    #     print '[predictOnWindows] results: {}'.format(results)
    #     t = results.keys()[0]
    #     keys = results[t].keys()
    #     writer.writerow(["Feature"]+results.keys())
    #     for key in keys:
    #         row = [key] + [d[key] for d in results.values()]
    #         writer.writerow(row)
    with open(UNIFIED_RESULTS_PATH,'w') as theFile:
        writer = csv.writer(theFile)
        print '[predictOnWindows] results: {}'.format(results)
        writer.writerow(["Algorithm", "Error"])
        for key, value in results.items():
            writer.writerow([key, value])
    os.system('touch timing/end_time')
    #plotData(linePerPatientData, labelsPerPatients)


if __name__=='__main__':
    predict()
