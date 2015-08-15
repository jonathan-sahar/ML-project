__author__ = 'Inspiron'

import numpy as np
from utils.constants import *
from utils.utils import readFileToFloat, castStructuredArrayToRegular
from optimize import optimizeHyperParams

X = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
y = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)

idxs = np.random.randint(len(X), size = len(X)/100)
X = X[idxs]
y = y[idxs]

# feature selection

# features = FeatureSelection.SelectFeatures(X, y)
# print "The selected feature are:", features

# hyperparameter tuning
X_array = castStructuredArrayToRegular(X)
pred = optimizeHyperParams(X_array, y, 'SVM')
print pred