__author__ = 'Inspiron'

from sklearn import datasets
import numpy as np
import FeatureSelection

iris = datasets.load_iris()
structuredData = np.core.records.fromarrays(iris.data.transpose(),
                                             names='Setosa, Versicolour, Virginica',
                                             formats = 'f8, f8, f8')

features = FeatureSelection.SelectFeatures(structuredData, iris.target)
print "the feature are"
print features