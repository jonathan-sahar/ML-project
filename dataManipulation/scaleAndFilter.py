 __author__ = 'Jonathan'
from sklearn.preprocessing import StandardScaler

# todo: complete me.
# this is meant to scale all the data coming out from feature creation (it will be scaled again inside the cross validation)
# and to remove time windows where the variance of the accelerometer/compass/whatever is too high
def scaleAndFilter(X, y):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    fields = []