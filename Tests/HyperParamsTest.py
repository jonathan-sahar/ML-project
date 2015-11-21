__author__ = 'Inspiron'

from utils.constants import *
from utils.utils import *
import modified_sklearn
from optimizationAndPrediction.predict import *
from modified_sklearn.cross_validation import LeavePLabelOut
from modified_sklearn.ensemble import *
import optimizationAndPrediction.FeatureSelection
import dataManipulation.createFeatureCSVs
from modified_sklearn.svm import SVC

def tuneAndTrainTest(estimatorType, data, labels, numFolds, patientIds, roundNum, estimator, lossFunction = lossFunction):

    folds = LeavePLabelOut(patientIds[0], p=2)
    errors = []

    counter = 0
    for trainIndices, testIndices in folds:

        #Tuning
        trainData = [data[i] for i in trainIndices]
        trainlabels = [labels[i] for i in trainIndices]
        testData = [data[i] for i in testIndices]
        testLabels = [labels[i] for i in testIndices]

        #Training
        if roundNum == 0:
            estimator.fit(trainData, trainlabels)
        else:
            estimator = optimizeHyperParams(trainData, trainlabels, estimatorType)

        #Testing
        errors.append(lossFunction(estimator, testData, testLabels))
    print np.array(errors).mean()


if __name__ == "__main__":
    selectedFeaturesTrainData = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
    trainlabels = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)
    patientIds = readFileAsIs(UNIFIED_AGGREGATED_PATIENT_NAMES_PATH)

    #estimatorsType = [("RF", RandomForestClassifier())]
    estimatorsType = [("SVM", SVC())]
    trainData = castStructuredArrayToRegular(selectedFeaturesTrainData)

    for (estimatorType, estimator) in estimatorsType:
        print "the error on {} with-out tune is: ".format(estimatorsType)
        tuneAndTrainTest(estimatorType, trainData, trainlabels, 8, patientIds, 0, estimator)
        print "the error on {} with tune is: ".format(estimatorsType)
        tuneAndTrainTest(estimatorType, trainData, trainlabels, 8, patientIds, 1, None)

