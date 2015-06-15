__author__ = 'Jonathan'

from itertools import product
import scipy.stats as stats
import scipy.fftpack as fft

from outSourcedModules.pyeeg import dfa
from outSourcedModules.entropy import entropy_ci
from utils.constants import *
from utils.utils import *
from utils.structuredDataConstants import accl_fields, psd_D


def getFieldNames(origNames, modifiers):
    '''
    :param origNames:
    :param modifiers:
    :return: names of new fields: each field appended with all modifiers.
    '''
    newFields = [str(x) + '_' + str(y) for x,y in product(origNames, modifiers)]
    return  (newFields)

def filter_fields_by_name(names, regex):
    '''
    :param names:
    :param regex:
    :return: an array of names that the regex matched on
    '''
    vmatch = np.vectorize(lambda x:bool(regex.match(x)))
    mask = vmatch(names)
    indices = np.where(mask)[0]
    return np.array(names)[indices]


def _mode(values): return stats.mode(values)[0][0]
def _range(a): return stats.tmax(a) - stats.tmin(a)
def _entropy(a): return entropy_ci(a, ENTROPY_RADIUS)
def _cross_correlation_accl(window, energy_type):
    '''
    :param window:
    :param energy_type: one of "low", "mid", "high"
    :return: cross correlation between movement in X and Y
    '''
    psd = str(psd_D[energy_type])
    a = window[:, accl_fields["x_PSD."+ psd]]
    b = window[:, accl_fields["y_PSD."+ psd]]
    return stats.pearsonr(a,b)[0]


def _cross_correlation_accl(window, energy_type): #TODO: add cross_entropy from theano
    return

def _DFA(a): return dfa(a, DFA_WINDOW_LEN)

def _per_window_mean_TKEO(a):
    values = [y**2 - x*z for x, y, z in zip(a[:-2],a[1:-1],a[2:])]
    return reduce(lambda x, y: x+y, values)/(len(a)-2)

def _zero_crossing_rate(a):
    positive = a > 0
    negative = ~positive
    v = ((positive[:-1] & negative[1:]) | (negative[:-1] & positive[1:]))
    w = np.where(v)
    return [len(w)]


#operates on sub windows
def numSamplesInFreqRange(window):
    names = window.dtype.names
    r = re.compile(r'([a-z]_PSD_\d+\b)')
    freqFields = filter_fields_by_name(window.dtype.names, r)
    headers = getFieldNames(freqFields, ['is_in_freq_range '])
    freqData = window[freqFields]
    freqData = castStructuredArrayToRegular(freqData)
    means = freqData.mean(0)
    boolean_indicators = ((FREQ_L < means) & (means < FREQ_H))
    return headers, boolean_indicators


# operates on windows
def numSubWindowsInFreqRange(window, aggregatedSubWindows):
    r = re.compile(r'(.*is_in_freq_range.*)')
    freqFields = filter_fields_by_name(aggregatedSubWindows.dtype.names, r)
    columns = [aggregatedSubWindows[field] for field in freqFields]
    counts  = [len(np.where(column)[0]) for column in columns]

    r = re.compile(r'([a-z]+_PSD_\d+\b)')
    origNames = filter_fields_by_name(window.dtype.names, r)
    headers = getFieldNames(origNames, ['num_subWindows_in_freq_range'])
    return headers, counts



#operates on entire data
def waveletCompressForAllColoumns(timeWindow, shortTimeWindows = None, windowType = 'long'):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return: matrix as a list of lists
    '''
    rows = []
    fieldNames = timeWindow.dtype.names
    headers = getFieldNames(fieldNames, ['DCT_coeff_'+ str(i) for i in range(1,NUM_COEFFS + 1)])
    coefficients = np.array([fft.dct(timeWindow[field]) for field in fieldNames]).T
    coefficient_means = np.mean(np.array(coefficients), 0)
    sorted_indices = sorted(range(len(coefficient_means)), key= lambda x: coefficient_means[x], reverse= True)
    top_indices = sorted_indices[:NUM_COEFFS]
    del sorted_indices
    mask = np.zeros(len(fieldNames), dtype = bool)
    mask[top_indices] = True
    # The following is the freq-domain representation after compression: compressed by taking the on-average-best coefficients
    top_coefficients = coefficients[mask, :]
    return headers,np.ravel(top_coefficients)

    # TODO: restore when we understand wavelet transform
    # # lists of lists of coefficients
    # app_coefients = []
    # detail_coefients = []
    # for column in timeWindow[1:].T:
    #     col_app_coefients, col_detail_coefients= pywt.dwt2(column, 'db2')
    #     app_coefients.append(col_app_coefients)
    #     detail_coefients.append(col_detail_coefients)
    # app_coefients_means = np.mean(np.array(app_coefients), 0)
    # sorted_indices = sorted(range(len(app_coefients_means)), key= lambda x: app_coefients_means[x])
    # top_indices = sorted_indices[:-NUM_COEFFS]
    # del sorted_indices
    # mask = np.zeros(len(app_coefients))
    # mask[sorted_indices] = True

stat_func_pointers = [
                     (stats.tmax, 'max')]\
    # ,
    #                  (stats.tmin,'min' ),
    #                  (stats.tmean,'mean'),
    #                  (stats.tstd, 'std'),
    #                  (stats.skew, 'skew'),
    #                  (stats.kurtosis, 'kurtosis'),
    #                  (np.nanmedian, 'median'),
    #                  (_mode, 'mode'),
    #                  (_per_window_mean_TKEO, 'mean_TKEO'),
    #                  (_zero_crossing_rate, 'zero_crossings')
    #                  ] #TODO add more functions

freq_domain_func_pointers = [()]

#operates in a window
def statisticsForAllColoumns(timeWindow, shortTimeWindows = None, windowType = 'long'):
    '''
    :param timeWindow:
    :param shortTimeWindows:
    :param windowType:
    :return: a list of names and an np.array of values
    '''
    names = [name for name in timeWindow.dtype.names if not name == "Is Sick"]
    fieldNames = getFieldNames(names, [touple[1] for touple in stat_func_pointers])
    row = np.atleast_2d([])
    columns = [timeWindow[fieldName] for fieldName in names]
    for column in columns:
        features_from_col = [np.array((func(column))) for func, _ in stat_func_pointers]
        v= np.array([features_from_col])
        row = np.hstack((row, v))
    row = np.array(row)
    return fieldNames, row

#meant for 'entire' data
def averageOnWindows(timeWindow, longTimeWindows = None, windowType = 'entire'):
    columns = longTimeWindows.dtype.names
    r = re.compile(r'(.*DCT.*)')
    fieldsToIgnore = filter_fields_by_name(columns,r)
    columns = [c for c in columns if c not in fieldsToIgnore]
    headers = getFieldNames(columns, ['average_on_windows'])
    means = [np.array(longTimeWindows[column]).mean() for column in columns]
    return headers, means

def statsForLongTimeWindow():
    return

