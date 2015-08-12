__author__ = 'Inspiron'

from sklearn import datasets
import numpy as np
import FeatureSelection
from utils.constants import *
from utils.utils import readFileToFloat, castStructuredArrayToRegular

# iris = datasets.load_iris()
# structuredData = np.core.records.fromarrays(iris.data.transpose(),
#                                              names='Setosa, Versicolour, Virginica, bla',
#                                              formats = 'f8, f8, f8, f8')
#
# features = FeatureSelection.SelectFeatures(structuredData, iris.target)

X = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
y = readFileToFloat(UNIFIED_AGGREGATED_LABELS_PATH, names = None)

# idxs = np.random.randint(len(X), size = len(X)/100)
# X = X[idxs]
# y = y[idxs]

features = FeatureSelection.SelectFeatures(X, y)
print "The selected feature are:", features

