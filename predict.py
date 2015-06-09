__author__ = 'Inspiron'

from constants import *
from random import shuffle
from utils import *
#from sklearn import svm #TODO other learners as well
import sklearn.svm


'''
for all patients,
line per entire data - predict by each feature of the line, all the features, and features of transform
average of all lines per 5 min of patient - get one line per patient - should be just another features in the 'line per patient'
lines per 5 min of data - predict by each feature, all the features.
'''


def getTransformationFeatures():
    return []


def svmPredictLinePerPatient(linePerPatientData,labelsPerPatients):
    predictor = sklearn.svm.SVC('linear')

    #todo restore
    # results = predictByFeatures(predictor, linePerPatientData, labelsPerPatients, True)

    #testing on all features at once:
    results = crossValidate(predictor, linePerPatientData, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)

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
    predictor = sklearn.svm.SVC('linear')
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

def predictByFeatures(predictor, linePerPatientData, labelsPerPatients, isEntire):
    results = []
    features = linePerPatientData.dtype.names

    for feature in features:
        linePerPatientMatrix = np.array(linePerPatientData)

        data = [] #TODO temp solution - ugly
        tmpData = list(linePerPatientMatrix[feature])
        for item in tmpData:
            data.append([item])

        #cross_validate
        #result = crossValidate(predictor, data, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)
        print data
        print '================================='
        print labelsPerPatients
        result = crossValidate(predictor, data, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)
        error = np.mean(result)
        results.append((error, feature))

    data = linePerPatientData
    #result = crossValidate(predictor, data, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)
    result = crossValidate(predictor, data, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)
    error = np.mean(result)
    results.append((error, 'all'))

    if isEntire:
        data = getTransformationFeatures(linePerPatientData)
        #result = crossValidate(predictor, data, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)
        result = crossValidate(predictor, data, labelsPerPatients, lossFunction, NUMBER_OF_FOLDS)
        error = np.mean(result)
        results.append((error, 'transformation'))

    return results


def plot(errorFeatureTupleList):
    sorted(errorFeatureTupleList, lambda x: x[1])
    print errorFeatureTupleList
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


def predict():
    #linePerPatientData = readFileToFloat(UNIFIED_ENTIRE_PATH)
    linePerPatientData = readFileToFloat(UNIFIED_ENTIRE_PATH)
    labelsPerPatients = readFileToFloat(UNIFIED_ENTIRE_LABELS_PATH, names = None)
    #labelsPerPatients = readFileAsIs(UNIFIED_ENTIRE_LABELS_PATH) #[0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1] #by the order in constants.py
    # labelsPerPatients = [0,1,1,1,0,1,1,0,0,1,1,0,0,0,1,1]

    #each result is a Dictionary with all learning Iterations (features, 'all', transformation')
    dataArray = castStructuredArrayToRegular(linePerPatientData)
    labelsList = labelsPerPatients
    svmLinePerPatientResults = svmPredictLinePerPatient(dataArray,labelsList)


    svmLinePerPatientResults = svmPredictLinePerPatient(linePerPatientData,labelsPerPatients)
    logisticRegLinePerPatientResults = logisticRegPredictLinePerPatient(linePerPatientData,labelsPerPatients)
    randomForestLinePerPatientResults = randomForestPredictLinePerPatient(linePerPatientData,labelsPerPatients)

    '''
    linePerFiveMinutesData = readFileToFloat(UNIFIED_AGGREGATED_PATH)
    LabelsPerLines = readFileAsIs(UNIFIED_AGGREGATED_LABELS_PATH)

    #each result is a Dictionary with all learning Iterations (features, 'all')
    svmLinePerFiveMinutesResults = svmPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    logisticRegLinePerFiveMinutesResults = logisticRegPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    randomForestLinePerFiveMinutesResults = randomForestPredictLinePerFiveMinutes(linePerFiveMinutesData,LabelsPerLines)
    '''

    plot(svmLinePerPatientResults)
    plot(logisticRegLinePerPatientResults)
    plot(randomForestLinePerPatientResults)

    '''
    plot(svmLinePerFiveMinutesResults)
    plot(logisticRegLinePerFiveMinutesResults)
    plot(randomForestLinePerFiveMinutesResults)
    '''

if __name__=='__main__':
    predict()
