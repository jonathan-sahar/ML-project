 __author__ = 'Jonathan'
from sklearn.preprocessing import StandardScaler
from utils.utils import filter_fields_by_name, castStructuredArrayToRegular
import re
import numpy as np

STDEV_THRESHOLD_UPPER = 0.5
STDEV_THRESHOLD_LOWER = 0.05
def filterLinesOnRegex(X, y, n, r = re.compile(r'([xyz]+_standard_deviation_mean)')):
    '''
    Removes time windows where the variance of the accelerometer/compass/whatever is too high
    currently looks at accelerometer std
    :param X: structured array
    :param y: labels
    :param n: names
    :return:
    '''
    scaler = StandardScaler()
    r = re.compile(r'([xyz]+_standard_deviation_mean)')
    fields = filter_fields_by_name(X.dtype.names, r)

    # filteredX is a scaled copy of the relevant features only
    filteredX = castStructuredArrayToRegular(X[fields])
    filteredX = scaler.fit_transform(filteredX)

    #mask is a 1D array with True for every line in filteredX where all values are within range
    mask = np.array([(filteredX < STDEV_THRESHOLD_UPPER) & (filteredX > STDEV_THRESHOLD_LOWER)])
    mask = np.squeeze(mask) #remove empty 3rd dimension
    mask = np.array([np.any(row) for row in mask])

    #indices are the indices (=line numbers) where mask is True

    indices = np.where(mask)
    return X[indices], y[indices], n[indices]






