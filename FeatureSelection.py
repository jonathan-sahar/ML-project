__author__ = 'Inspiron'

from utils.constants import *
from utils.utils import *
import sklearn
import numpy as np
from sklearn.feature_selection import *


def SelectFeatures(featuresStructuresArray, labels):
    estimator = sklearn.linear_model.LogisticRegression('l2', False)

    featureNames = featuresStructuresArray.dtype.names
    featureData = castStructuredArrayToRegular(featuresStructuresArray)

    featuresSelector = RFECV(estimator, cv=8)
    featuresSelector.fit(featureData , labels)
    selectedIndices = featuresSelector.get_support()

    selectedFeatures = np.array(featureNames)[selectedIndices]
    return selectedFeatures


#SCALED_UNIFIED_ENTIRE_DATA_PATH
