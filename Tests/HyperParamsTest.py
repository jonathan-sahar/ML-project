__author__ = 'Inspiron'

from utils.constants import *
from utils.utils import *
import sklearn
import predict
from sklearn.cross_validation import LeavePLabelOut
from sklearn.ensemble import *
import FeatureSelection
import createFeatureCSVs



def tuneAndTrain(estimatorType, data, labels, numFolds, patientIds, roundNum, estimator, lossFunction = predict.lossFunction):
    folds = LeavePLabelOut(patientIds, p=2)
    errors = []
    for trainIndices, testIndices in folds:
        #if np.all(trainlabels == trainlabels[0]): #can't train on elements that are all from the same group
        #    continue

        #Tuning
        trainData = [data[i] for i in trainIndices]
        trainlabels = [labels[i] for i in trainIndices]
        testData = [data[i] for i in testIndices]
        testLabels = [labels[i] for i in testIndices]

        #Training
        if roundNum == 0:
            estimator.fit(trainData, trainlabels)
        else:
            estimator = predict.optimizeRandomForestHyperParameters(estimatorType, trainData, trainlabels)

        #Testing
        errors.append(lossFunction(estimator, testData, testLabels))
    print np.array(errors).mean()


if __name__ == "__main__":
    selectedFeaturesTrainData = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
    trainlabels = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)
    patientIds = readFileToFloat(UNIFIED_AGGREGATED_PATIENT_NAMES_PATH, names = None)

    estimatorsType = [("RF", RandomForestClassifier())]

    for (estimatorType, estimator) in estimatorsType:
        print "the error on {} with-out tune is: ".format(estimatorsType)
        tuneAndTrain(estimatorType, selectedFeaturesTrainData, trainlabels, 8, patientIds, 0, estimator)
        print "the error on {} with tune is: ".format(estimatorsType)
        tuneAndTrain(estimatorType, selectedFeaturesTrainData, trainlabels, 8, patientIds, 1, None)

