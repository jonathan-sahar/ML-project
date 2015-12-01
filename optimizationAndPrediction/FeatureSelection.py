__author__ = 'Inspiron'

from utils.constants import *
from utils.utils import *
from modified_sklearn.linear_model import LogisticRegression
import numpy as np
from modified_sklearn.feature_selection import RFECV
from modified_sklearn.linear_model import LogisticRegression

def SelectFeatures(featuresStructuresArray, labels):
    estimator = LogisticRegression('l2', False)

    featureNames = featuresStructuresArray.dtype.names
    featureData = castStructuredArrayToRegular(featuresStructuresArray)

    featuresSelector = RFECV(estimator, cv=5)
    featuresSelector.fit(featureData , labels)
    selectedIndices = featuresSelector.get_support()

    selectedFeatures = np.array(featureNames)[selectedIndices]
    return selectedFeatures


#SCALED_UNIFIED_ENTIRE_DATA_PATH
