__author__ = 'Inspiron'

from random import shuffle

from utils.constants import *
from utils.utils import *

#from sklearn import svm #TODO other learners as well
import sklearn.svm
import sklearn.ensemble
import sklearn.linear_model
from FeatureSelection import SelectFeatures
from sklearn.preprocessing import StandardScaler

'''
for all patients,
line per entire data - predict by each feature of the line, all the features, and features of transform
average of all lines per 5 min of patient - get one line per patient - should be just another features in the 'line per patient'
lines per 5 min of data - predict by each feature, all the features.
'''



def lossFunction(estimator, X, y):
    loss = 0.0
    for data,label in zip(X,y):
        if estimator.predict(data)[0] != label:
            loss += 1
    loss = loss / len(X)
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


def plot(errorFeatureTupleDict, resultPath):
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


def predictOnWindows():
    # learning on data divided into time windows
    #==============================================================================================
    linePerFiveMinutesData = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
    linePerFiveMinutesLabels = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)

    selectedFeatures = SelectFeatures(linePerFiveMinutesData, linePerFiveMinutesLabels)
    print "the selected features are: ", selectedFeatures
    selectedFeaturesData = [linePerFiveMinutesData[f] for f in selectedFeatures]
    #==============================================================================================


    #each result is a Dictionary with all learning Iterations (features, 'all')
    #==============================================================================================
    predictor = sklearn.svm.SVC()
    svmLinePerFiveMinutesResults  = predictByFeatures(predictor, selectedFeaturesData,linePerFiveMinutesLabels, False)
    print "svm on windows is done!"

    predictor = sklearn.linear_model.LogisticRegression('l2', dual = False, multi_class='ovr')
    logisticRegLinePerFiveMinutesResults = predictByFeatures(predictor, selectedFeaturesData,linePerFiveMinutesLabels, False)
    print "logisticReg on windows is done!"

    predictor = sklearn.linear_model.LogisticRegression('l1', dual = False, multi_class='ovr')
    logisticRegLinePerFiveMinutesResults = predictByFeatures(predictor, selectedFeaturesData,linePerFiveMinutesLabels, False)
    print "logisticReg on windows is done!"

    predictor = sklearn.ensemble.RandomForestClassifier(75) #65 is aprox the sqrt of the fiveMinutes we have in FIRSTDATA
    randomForestLinePerFiveMinutesResults = predictByFeatures(predictor, selectedFeaturesData,linePerFiveMinutesLabels, False)
    print "randomForest on windows is done!"


    print "plotting..."
    plot(svmLinePerFiveMinutesResults, SVM_RES_WINDOWS_PATH)
    plot(logisticRegLinePerFiveMinutesResults, LOGISTIC_RES_WINDOWS_PATH)
    plot(randomForestLinePerFiveMinutesResults, FOREST_RES_WINDOWS_PATH)

def predict():
    try:
        os.mkdir(RESULTS_FOLDER)
    except WindowsError:
        pass

    # predictOnEntire()
    predictOnWindows()





    #plotData(linePerPatientData, labelsPerPatients)

if __name__=='__main__':
    predict()
