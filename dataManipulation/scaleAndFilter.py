from sklearn.preprocessing import StandardScaler
from utils.utils import filter_fields_by_name
import re
# todo: complete me.
# this is meant to scale all the data coming out from feature creation (it will be scaled again inside the cross validation)
# and to remove time windows where the variance of the accelerometer/compass/whatever is too high

STDEV_THRESHOLD = 0.5
def scaleAndFilter(X, y):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    r = re.compile(r'([xyz]+_standard_deviation_mean)')
    fields = filter_fields_by_name(X.dtype.names, r)
    mask = X[fields] > STDEV_THRESHOLD
