__author__ = 'Inspiron'

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import LeavePLabelOut
import numpy as np

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

def twoStepsTest():
    X = [[0.4,0.3], [0.2,0.2], [0.6,0.7], [0.2,0.8]]
    y = [0,0,1,1]
    estimator = LogisticRegression().fit(X,y)
    names = ['er', 'qa', 'qa', 'er']
    testData = [[0.5,0.3], [0.2,0.2], [0.2,0.3], [0.5,0.4]]
    testLabels = [0,1,1,0]
    twoStepsLoss(estimator, testData, testLabels, names)

if __name__ == "__main__":
    twoStepsTest()