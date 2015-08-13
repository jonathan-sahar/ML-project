__author__ = 'Inspiron'


from sklearn.preprocessing import StandardScaler
from utils.utils import *
from utils.constants import *

linePerFiveMinutesData = readFileToFloat(UNIFIED_AGGREGATED_DATA_PATH)
dataArray = castStructuredArrayToRegular(linePerFiveMinutesData)

scaler = StandardScaler()
scaledData = scaler.fit_transform(dataArray)

print scaledData

